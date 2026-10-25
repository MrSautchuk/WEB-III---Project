# Guia de Contribuição do Grupo — Hub de Marketplaces

Este documento estabelece o contrato interno de trabalho e colaboração da equipe para o desenvolvimento do **Hub de Marketplaces** na disciplina de **Web III (2026/2) — FATEC Olímpia**. Todos os integrantes devem ler, compreender e seguir rigorosamente estas diretrizes.

---

## 1. Fluxo de Trabalho Git (Git Flow & Branches)

### 1.1 Política de Branches

- **`main`** — branch principal e estável de produção. É **estritamente protegida**: nunca realize commits ou pushes diretos na `main`. Todo código entra na `main` exclusivamente via Pull Request aprovado com CI verde.
- **`develop`** *(opcional/integração)* — branch de consolidação preliminar de features antes da release de sprint.
- **`feature/nome-da-tarefa`** — branch obrigatória para o desenvolvimento de novas funcionalidades ou módulos.
- **`fix/nome-da-correcao`** — branch específica para correções cirúrgicas de bugs e defeitos.
- **`docs/nome-do-documento`** — branch reservada exclusivamente para criação ou atualização de documentação.
- **`chore/tarefa-manutencao`** — branch destinada a tarefas de infraestrutura, dependências ou configurações.

### 1.2 Convenção de Nomenclatura de Branches

Utilize letras minúsculas, hífen como separador e prefixo semântico:
```bash
feature/integracao-mercadolivre-oauth
feature/webhook-receptor-pedidos
fix/resiliencia-retry-timeout-api
docs/atualizar-manual-usuario
chore/dependencias-drf-spectacular
```

---

## 2. Padrão de Mensagens de Commit (Conventional Commits)

Todas as mensagens de commit devem seguir o padrão **Conventional Commits**:
```
<tipo>(<escopo opcional>): <descrição no imperativo e em minúsculas> [US-XX]
```

### Tipos Permitidos:
- **`feat`**: nova funcionalidade para o usuário ou API.
- **`fix`**: correção de bug ou tratamento de exceção.
- **`docs`**: alterações em arquivos de documentação (`README.md`, `SECURITY.md`, etc.).
- **`style`**: formatação de código (espaçamento, vírgulas) sem alteração de lógica.
- **`refactor`**: refatoração de código sem alteração no comportamento funcional.
- **`test`**: criação, expansão ou ajuste de testes automatizados.
- **`chore`**: manutenção de build, dependências (`requirements.txt`), linters ou CI.

### Exemplos Válidos:
```text
feat(marketplaces): implementar handler de webhook concorrente do Mercado Livre [US-08]
fix(auth): tratar expiracao de refresh token jwt na api de login [US-12]
docs(readme): reestruturar topicos no padrao oficial da fatec [US-23]
test(pedidos): adicionar testes de integracao para sincronizacao assincrona [US-15]
chore(config): alinhar .env.example com variaveis institucionais [US-35]
```

---

## 3. Diretrizes para Pull Requests (PRs)

### 3.1 Checklist Antes de Abrir o PR
Antes de enviar suas alterações para o repositório remoto:
- [ ] O código executa perfeitamente no ambiente local sem erros de runtime.
- [ ] Todos os **213 testes automatizados** continuam passando (`python manage.py test` ou `pytest`).
- [ ] O código foi formatado e inspecionado pelo linter (`ruff check .` e `ruff format .`).
- [ ] Não há chaves privadas, senhas reais ou arquivos `.env` incluídos no commit (`git diff --staged` verificado).
- [ ] A branch local está atualizada em relação à `main` (`git pull origin main --rebase`).

### 3.2 Estrutura do Pull Request
Ao abrir o PR no GitHub:
- **Título**: Resumo no padrão Conventional Commit (ex: `feat(pedidos): adicionar filtro multi-loja [US-14]`).
- **Descrição**:
  1. **O que foi feito**: resumo objetivo das alterações técnicas.
  2. **Por que foi feito**: motivação e valor de negócio/acadêmico.
  3. **User Story vinculada**: link direto para o card no Taiga.
  4. **Como testar**: comandos ou passos na interface para reproduzir a validação.
  5. **Evidências visuais**: capturas de tela caso haja alterações de interface (HTML/CSS).
- **Reviewers**: Atribuir obrigatoriamente **pelo menos 1 colega revisor** e o Scrum Master da sprint.

### 3.3 Regras para Merge
Nenhum PR poderá ser mesclado na branch `main` sem satisfazer:
1. **Aprovação Formal**: Mínimo de **1 aprovação (Review Approved)** de outro integrante do grupo.
2. **Pipeline de CI Verde**: Execução com 100% de sucesso de todos os workflows automatizados (`ci.yml`, `secret-scan.yml`).
3. **Ausência de Conflitos**: Resolução prévia de qualquer divergência com a branch `main`.
4. **Estratégia de Merge**: Utilizar preferencialmente **Squash and Merge** para manter o histórico da `main` linear, limpo e rastreável.

---

## 4. Padrões de Código e Arquitetura

### 4.1 Python
- **Linter & Formatação**: Aderência às regras configuradas no [Ruff](https://docs.astral.sh/ruff/).
- **Convenção de Nomes**:
  - Variáveis, métodos e funções: `snake_case` (ex: `calcular_comissao_marketplace()`).
  - Classes e Models: `PascalCase` (ex: `ContaMarketplace`, `PedidoVenda`).
  - Constantes globais: `UPPER_SNAKE_CASE` (ex: `STATUS_PEDIDO_FATURADO`).
  - Atributos e métodos protegidos/privados: prefixo `_` (ex: `_autenticar_canal()`).
- **Docstrings**: Obrigatórias para classes de serviço, modelos de dados e métodos de integração externa.

### 4.2 Django & Arquitetura
- **Salvaguarda de Migrações**: Migrações (`migrations/`) fazem parte do versionamento do projeto. **Nunca delete migrações existentes** nem altere migrações já consolidadas na branch `main`.
- **Models**: Todos os models devem ter método `__str__()` significativo e classe `Meta` com `ordering` e `verbose_name`.
- **Views & Endpoints**: Rotas devem possuir parâmetro `name=` explícito para suporte a `reverse()`.
- **Isolamento de Negócio**: Lógicas de integração externa devem residir na camada de serviços (`services.py` ou `connectors/`), nunca acopladas diretamente dentro de views ou models.

---

## 5. Política Institucional de Uso de IA Generativa

O projeto observa integralmente a **Política de IA em 4 Níveis da Disciplina de Web III (FATEC)**:

- **Nível 1 (Livre):** Resolução de dúvidas conceituais, tradução e análise de mensagens de erro, sugestões de nomes de variáveis e revisão ortográfica/gramatical.
- **Nível 2 (Com Declaração Obrigatória):** Códigos ou blocos estruturais gerados com auxílio de IA exigem obrigatoriamente:
  - Manutenção do comentário na **primeira linha do arquivo**:
    ```python
    # Os códigos foram gerados com auxilio de I.A.
    ```
  - Menção declarativa na descrição do Pull Request e do card do Taiga.
- **Nível 3 (Estritamente Proibido):** Avaliações individuais, provas práticas e defesa oral de Sprint Review.
- **Nível 4 (Metacompetência Técnica):** Domínio de Engenharia de Prompt para geração de soluções modulares, seguras e testáveis.

> ⚠️ **Atenção:** Cada integrante deve ser capaz de explicar detalhadamente, linha a linha, o funcionamento técnico do código submetido em seu Pull Request durante a Sprint Review oral com o professor.

---

## 6. Papéis Scrum do Grupo

Os papéis são dinâmicos e **rotativos a cada sprint**, garantindo que todos os integrantes vivenciem as diferentes responsabilidades metodológicas:

- **Product Owner (PO):** Interface de produto, alinhamento dos requisitos com o template do docente, priorização do backlog de User Stories e validação dos critérios de aceite.
- **Scrum Master (SM):** Facilitação das cerimônias, remoção de impedimentos técnicos, monitoramento do fluxo do Taiga e controle da política de branches e PRs.
- **Time de Desenvolvimento (Dev Team):** Engenharia de software, codificação incremental, cobertura de testes, revisão cruzada de código e documentação.

### 6.1 Matriz de Papéis Rotativos por Sprint

| Sprint | Período / Foco | Product Owner (PO) | Scrum Master (SM) | Time de Desenvolvimento |
| :--- | :--- | :--- | :--- | :--- |
| **Sprint 1** | Fundamentos & Setup | `Allan Sautchuk` | `Oscar Neris` |
| **Sprint 2** | Integrações & Mocking | `Oscar Neris` | `Davidson Willis` | `Vando Souza` , `Allan Sautchuk` , `Rafael Neves` , `Guilherme Vilela` |
| **Sprint 3 (Atual)** | Adequação ao Template & Governança | `Allan Sautchuk` | `Rafael Neves` | `Guilherme Vilela` |
| **Sprint 4** | Deploy, NoSQL & Entrega Final | `Oscar Neris` |

---

## 7. Cerimônias Ágeis

- **Sprint Planning**: Reunião no início da sprint para estimativa e seleção de cards do Product Backlog para a Sprint Backlog no Taiga.
- **Daily Assíncrona**: Acompanhamento diário via canal da equipe e atualização do status dos cards no Taskboard do Taiga.
- **Sprint Review**: Demonstração funcional do software em funcionamento para o professor no encerramento da sprint.
- **Sprint Retrospective**: Avaliação interna do grupo baseada nos pilares: *O que manter?*, *O que melhorar?*, *O que começar?* e *O que parar?*.

---

## 8. Critérios de Aceite Globais (Definition of Done - DoD)

Uma User Story só poderá transitar para o status **Done** no Taiga quando cumprir:

- [ ] Código integrado na branch `main` via Pull Request aprovado.
- [ ] 100% dos testes da suíte passando sem quebra ou regressão.
- [ ] Cobertura de código testada e superior à régua mínima estipulada pela disciplina (>= 40%).
- [ ] Revisão de código concluída por pelo menos um colega de equipe.
- [ ] Documentação correspondente atualizada nos arquivos de governança ou na pasta `docs/`.
- [ ] Ausência de segredos ou vulnerabilidades reportadas pelas ferramentas de auditoria.
- [ ] Card e tarefas associadas devidamente fechadas no Taiga.
