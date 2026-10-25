# ADR 014 — Extrair um Service da view AnuncioToggleIgnorarView

> **Declaração de Integridade Acadêmica:** Este conteúdo foi produzido com auxílio de IA.

## Contexto
Na arquitetura do Hub, a view baseada em classe `AnuncioToggleIgnorarView` (localizada em `apps/anuncios/views.py`, linhas 756 a 819) é responsável por alternar a decisão do operador entre sincronizar ativamente ou descartar/cancelar alterações pendentes de um anúncio comercial.

Ao inspecionar sua implementação, identificamos que ela viola o Princípio da Responsabilidade Única (SRP) ao misturar quatro responsabilidades distintas em um único método `post`:

1. **Acesso a dados, infraestrutura HTTP e autorização**:
   - Trata a requisição HTTP POST e captura parâmetros de rota;
   - Realiza validações de autenticação (`LoginRequiredMixin`), módulo contratual (`ModuloRequeridoMixin`), papéis RBAC (`pode_disparar_sincronizacao`, `usuario_is_dev`) e isolamento horizontal multi-tenant (`anuncio.conta.loja_id != perfil.loja_id`).

2. **Regra de negócio, cálculo de cota e decisão de domínio (Máquina de Estados)**:
   - Captura snapshots em memória dos valores correntes (`preco_venda`, `estoque_publicado`);
   - Invoca o cálculo de cota física disponível a partir da composição de inventário (`anuncio.calcular_cota_disponivel()`);
   - Aplica a lógica condicional de transição de status (State Pattern / ADR-011): se o anúncio estiver `CANCELADO`, avalia se há divergência entre a cota calculada e o estoque publicado. Caso divirja, decide transitar para `PENDENTE`; caso coincida, transita para `ENVIADO`. Se o anúncio não estiver cancelado, força a transição para `CANCELADO`;
   - Define a semântica do evento de negócio e a justificativa textual do motivo da operação.

3. **Persistência transacional e auditoria**:
   - Persiste a alteração de status na tabela `Anuncio` (`save(update_fields=['status_sincronizacao', 'atualizado_em'])`);
   - Instancia e grava a trilha de auditoria na tabela `HistoricoSincronizacaoAnuncio` com os snapshots numéricos de preço e estoque (anteriores e propostos), usuário responsável e motivo.

4. **Montagem da resposta e navegação da interface**:
   - Dispara mensagens de notificação flash ao usuário (`messages.success()` / `messages.info()`);
   - Inspeciona o cabeçalho `HTTP_REFERER` e constrói o redirecionamento HTTP (`redirect(referer)` com fallback para `anuncio_detail`).

### O problema de design
A regra de negócio central — a máquina de estados que rege o ciclo de vida do anúncio, a verificação de divergência de estoque e o registro formal de auditoria — está **aprisionada dentro da view**.

Como consequência:
- Não conseguimos testar essa lógica de domínio de forma isolada e rápida; qualquer teste unitário é obrigado a simular uma requisição HTTP completa (com middlewares, sessões, cookies e roteador de URL do Django);
- A regra de transição não pode ser reaproveitada por outros pontos do sistema, como comandos de linha de comando (`management commands`), tarefas assíncronas em lote (Celery) ou futuras APIs REST/GraphQL.

---

## Decisão
Vamos extrair toda a lógica de tomada de decisão de transição de estado, reconciliação de cota física, persistência e gravação de histórico de auditoria para a **camada de serviços (`apps/anuncios/services.py`)**, criando o serviço `AnuncioCicloService` (ou método especializado em `AnuncioSincronizacaoService`):

```python
class AnuncioCicloService:
    @classmethod
    def alternar_status_ignorar(cls, anuncio: Anuncio, usuario) -> Tuple[str, str, str]:
        """
        Executa a máquina de estados para cancelamento ou reativação de sincronização do anúncio.
        Retorna uma tupla contendo: (novo_status, tipo_mensagem, texto_mensagem).
        """
        preco_ant = anuncio.preco_venda
        cota_ant = anuncio.estoque_publicado
        cota_atual = anuncio.calcular_cota_disponivel()

        if anuncio.status_sincronizacao == 'CANCELADO':
            if anuncio.estoque_publicado != cota_atual:
                anuncio.status_sincronizacao = 'PENDENTE'
            else:
                anuncio.status_sincronizacao = 'ENVIADO'
            tipo_msg = 'success'
            texto_msg = f"Sincronização reativada para o anúncio [{anuncio.item_id_externo}] (Status: {anuncio.get_status_sincronizacao_display()})."
            motivo = "Reativação da sincronização pelo operador"
        else:
            anuncio.status_sincronizacao = 'CANCELADO'
            tipo_msg = 'info'
            texto_msg = f"O anúncio [{anuncio.item_id_externo}] foi marcado como CANCELADO para sincronizações."
            motivo = "Sincronização cancelada / descartada pelo operador"

        anuncio.save(update_fields=['status_sincronizacao', 'atualizado_em'])

        HistoricoSincronizacaoAnuncio.objects.create(
            anuncio=anuncio,
            status_resultante=anuncio.status_sincronizacao,
            preco_anterior=preco_ant,
            preco_proposto=preco_ant,
            estoque_anterior=cota_ant,
            estoque_proposto=cota_atual,
            usuario=usuario,
            motivo=motivo
        )

        return anuncio.status_sincronizacao, tipo_msg, texto_msg
```

Com essa extração, a view `AnuncioToggleIgnorarView` passa a ter **responsabilidade única da camada Web**:
1. Validar autenticação, permissões RBAC e tenancy da requisição;
2. Recuperar a instância do anúncio com `get_object_or_404`;
3. Delegar a operação para o service: `_, tipo_msg, texto_msg = AnuncioCicloService.alternar_status_ignorar(anuncio, request.user)`;
4. Emitir a notificação através de `getattr(messages, tipo_msg)(request, texto_msg)`;
5. Redirecionar para o `HTTP_REFERER` ou tela de detalhes.

---

## Alternativa descartada
A equipe considerou e descartou formalmente duas alternativas:

1. **Deixar a regra na view e testá-la com o Django Test Client (`client.post(...)`)**:
   - *Por que foi descartada*: O teste ficaria lento e excessivamente acoplado à camada web (dependendo de middleware de sessão, autenticação HTTP, resolução de URLs e cookies). Além disso, a regra continuaria inacessível para ser invocada a partir de outras partes do sistema, como comandos de rotina noturna em lote, rotinas de conciliação ou endpoints de API REST.

2. **Mover a lógica diretamente para o Model `Anuncio` (padrão *Fat Model*, ex.: `anuncio.toggle_ignorar(usuario)`)**:
   - *Por que foi descartada*: Violaria a coesão do modelo de domínio. O model `Anuncio` passaria a instanciar e salvar modelos secundários (`HistoricoSincronizacaoAnuncio`), lidando com a gestão do usuário da requisição e orquestrações procedurais de ciclo de vida. Isso tornaria o model inchado (*God Model*), ferindo a separação entre entidades de dados e orquestradores de fluxo.

---

## Consequência
### Ganhos esperados:
- **Testabilidade desacoplada**: A máquina de transição de status e o cálculo comparativo de cota tornam-se 100% testáveis através de testes unitários puros em milissegundos, sem necessidade de instanciar clientes HTTP, sessões ou rotas web.
- **Reusabilidade arquitetural**: A mesma regra pode ser chamada por tarefas assíncronas (Celery), scripts CLI administrativos (`manage.py`) ou endpoints de API.
- **Camada Web enxuta e coesa**: A view passa de mais de 60 linhas para cerca de 15 linhas limpas, concentrando-se exclusivamente em segurança de entrada (RBAC/Tenant) e resposta HTTP.

### Custos e limitações:
- Introdução de mais uma camada explícita a ser compreendida pela equipe (`services.py`).
- Necessidade de definir contratos claros de retorno entre Service e View (como DTOs, tuplas ou dicionários) para repasse de mensagens à interface.

---

## Status
Planejado — a extração será feita na sprint. (Registrando a decisão de design.)
