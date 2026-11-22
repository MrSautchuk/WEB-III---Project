# ADR 018 — Formalização do Padrão Facade sobre a Camada de Serviços

- **Data:** 2026-11-22
- **Status:** Em implantação (Semi-implantado — refatoração planejada na Sprint 3)
- **Decisores:** Equipe Hub Central de Marketplaces (Allan, Davidson, Guilherme, Oscar, Rafael, Vando)

> **Declaração de Integridade Acadêmica:** Este conteúdo foi produzido com auxílio de IA.

## Contexto

Diversos fluxos críticos do Hub Central orquestram múltiplos subsistemas em sequência (validação de assinatura/idempotência, consulta a conectores, locks pessimistas `select_for_update()`, atualização de estoque/preço em kits `AnuncioComposicao` e gravação de `LogAuditoria`):
- Parte do sistema já concentra essa orquestração em classes de serviço que funcionam na prática como **Facades**, como `MercadoLivreWebhookService.processar_notificacao` (`apps/marketplaces/services.py`), `ProcessamentoPedidoService.processar_pedido_venda` (`apps/pedidos/services.py`), `AnuncioImportacaoService` / `AnuncioSincronizacaoService` (`apps/anuncios/services.py`), `SimuladorPromocionalService` (`apps/financeiro/services.py`) e `MockDataService` (`apps/mockar_dados/services.py`).
- Entretanto, o padrão está **semi-implantado**, pois outras views e handlers ainda orquestram múltiplos subsistemas diretamente: `ProdutoSincronizarPrecoView.post`, `ProdutoSincronizarPrecoLoteView.form_valid` e `PublicarAnuncioView.post` (`apps/catalogo/views.py`), `AnuncioToggleIgnorarView.post` (`apps/anuncios/views.py`, documentada no `ADR-015`) e `disparar_sincronizacao_anuncios_produto` (`apps/anuncios/signals.py`).

## Decisão

**APLICAMOS / VAMOS FORMALIZAR o padrão Facade:** o padrão **cabe** e já está **semi-implantado** pela Service Layer; decidimos **alterar e concluir a implantação** migrando a orquestração residual das views legadas (`catalogo/views.py` e `anuncios/views.py`) e signals para pontos únicos de fachada/serviço, garantindo que a camada web apenas receba a requisição, delegue e devolva a resposta HTTP.

## Justificativa e Alternativa Descartada

- **Por que cabe:** Centralizar a ordem dos passos (buscar dados, travar estoque, chamar conector, registrar histórico/auditoria) em uma fachada explícita elimina duplicação entre views web, webhooks e futuras rotas da API REST, mantendo as views finas (SRP).
- **Alternativa descartada:** Deixar a orquestração espalhada em `views.py` e `signals.py` ou criar uma única "SuperFacade" para todo o projeto — a primeira perpetua acoplamento web + regra de negócio, e a segunda criaria um *God object* que concentra lógica em vez de apenas **delegar** aos subsistemas.
- **Delimitação em Python/Django:** A Facade **delega** aos services/models especialistas e não reimplementa regras de domínio internamente; em Django, essa fachada pode coexistir com a convenção `*Service` ou adotar sufixo `*Facade` nos fluxos multi-módulo.

## Consequências

- **Positivas:** Views e signals mais simples e fáceis de testar; fluxo único reaproveitável tanto pelos templates Django quanto por endpoints DRF.
- **Custo / Plano de ação:** Requer extração controlada da orquestração em `apps/catalogo/views.py` e `apps/anuncios/views.py` (cards de refatoração abertos na Sprint 3 do Taiga).

## Commit

Rastreável a partir do commit de consolidação do Caderno de Design e da refatoração planejada na Sprint 3 (`main`).
