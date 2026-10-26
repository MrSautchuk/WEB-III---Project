# Política de Segurança — Hub de Marketplaces

## Versões Suportadas

Atualmente, apenas as seguintes versões da aplicação e da stack recebem atualizações de segurança e correções ativas:

| Componente | Versão Suportada | Status de Suporte |
| :--- | :--- | :--- |
| **Hub de Marketplaces** | `v1.0.x` (Branch `main`) | :white_check_mark: Suportado |
| **Python** | `>= 3.12` | :white_check_mark: Suportado |
| **Django** | `>= 5.1` | :white_check_mark: Suportado |
| **Versões Anteriores** | `< 1.0.0` | :x: Não Suportado |

---

## Recursos de Segurança Ativos neste Repositório

Este repositório adota múltiplos mecanismos automáticos de prevenção e conformidade com o padrão institucional FATEC:

- **Dependabot** — monitora dependências vulneráveis no `requirements.txt` e abre Pull Requests semanais de correção automática (ver `.github/dependabot.yml`).
- **GitHub Secret Scanning** — nativo para repositórios públicos, detecta chaves de API, credenciais e tokens vazados.
- **Gitleaks CI** — camada extra de varredura estática de segredos que executa a cada push ou PR (ver `.github/workflows/secret-scan.yml`).
- **pip-audit** — auditoria de segurança das dependências Python contra a base de dados do PyPA/OSV a cada commit na pipeline de CI (ver `.github/workflows/ci.yml`).
- **Criptografia Fernet em Repouso** — tokens OAuth e credenciais sensíveis gravadas em banco são criptografados com chave AES de 32 bytes (`FIELD_ENCRYPTION_KEY`).

---

## Reportando uma Vulnerabilidade

Se você identificou uma vulnerabilidade de segurança neste projeto:

1. **NÃO abra uma issue pública** — vulnerabilidades reportadas em issues públicas ficam visíveis para todos, expondo potenciais riscos antes da correção.
2. **Comunique confidencialmente aos responsáveis:**
   - **Professor da Disciplina:** `jose.ceron@cps.sp.gov.br`
   - **Responsável de Segurança / Equipe do Projeto:** `allan.sautchuk@aluno.cps.sp.gov.br | oscar.neris@aluno.cps.sp.gov.br | guilherme.vilela@aluno.cps.sp.gov.br | rafael.neves@aluno.cps.sp.gov.br | davidson.willis@aluno.cps.sp.gov.br | vando.souza@aluno.cps.sp.gov.br`
3. Se preferir, utilize o recurso de divulgação privada do GitHub: na aba **Security → Report a vulnerability**.
4. **SLA de Resposta:** Nossa equipe acusará o recebimento e iniciará a triagem do relatório em até **48 horas úteis**, mantendo o relator informado sobre a remediação e o lançamento do patch corretivo (disclosure responsável).

---

## O que Fazer se Commitar um Segredo por Engano

Acontece com a maioria dos desenvolvedores pelo menos uma vez. Não entre em pânico, mas aja com agilidade:

1. **Revogue e rotacione o segredo imediatamente** no serviço de origem (Mercado Livre Developers, MongoDB Atlas, chaves de API, console em nuvem). Trocar o segredo é a **única mitigação real** — remover o commit do Git NÃO invalida o segredo, pois ele já pode ter sido capturado em mirrors ou caches.
2. **Avise o time e o professor** para registrar o incidente (aprendizado da equipe, sem penalidade se reportado com transparência e prontidão).
3. **Remova o segredo do histórico local do Git:**
   ```bash
   # Se foi no último commit (ainda não enviado)
   git reset HEAD~1
   # Edite o arquivo, remova o segredo, garanta que esteja no .gitignore
   git add .
   git commit -m "fix(sec): remove segredo commitado por engano"
   git push --force-with-lease
   ```
4. **Se o commit já foi enviado para a branch `main` ou compartilhada:**
   * Alerte todos os membros da equipe imediatamente.
   * Proceda com a rotação de todas as chaves e, se necessário, use ferramentas especializadas sob supervisão.
5. **Atualize o `.gitignore`** adicionando o padrão de arquivo ou extensão para impedir que a falha se repita.

---

## Boas Práticas da Equipe

- **Nunca escreva segredos diretamente no código-fonte.** Sempre utilize variáveis de ambiente gerenciadas via `.env` carregadas por `python-decouple`.
- **Nunca commite arquivos `.env` ou `.env.local`** (ambos estão blindados no `.gitignore`).
- **Verifique seus arquivos antes de cada push:** crie o hábito de executar `git diff --staged` para inspecionar exatamente o que está sendo empacotado.
- **Rotacione segredos periodicamente** — mesmo sem a ocorrência de incidentes.
- **Configure autenticação de dois fatores (2FA)** obrigatória na conta do GitHub de todos os integrantes da equipe.
