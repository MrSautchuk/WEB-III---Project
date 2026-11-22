# ADR 015 — Arquitetura de Apresentação, Temas Visuais e Ergonomia Operacional


> **Declaração de Integridade Acadêmica:** Este conteúdo foi produzido com auxílio de IA.

## 1. Contexto

Operadores de armazém e gestores de e-commerce atuam em cenários variados — desde telas industriais de baixa luminosidade e coletores móveis em estoque até desktops de escritório. A interface exigia suporte a temas visuais ergonômicos, navegação sequencial intuitiva e responsividade estrita sem quebras de layout.


## 2. Decisão

**Fizemos melhorias visuais importantes na parte de front-end:**

  - **Grid na Home:** Organizamos a página inicial em blocos( grid 4x2) para ficar bem fácil de achar os módulos.
  - **Menu organizado:** Consertamos a barra de navegação para não quebrar o layout (overflow) em telas menores.
  - **Modos de Tema:** Adicionamos um salvamento no navegador (localStorage) que permite alternar entre 4 temas visuais: Padrão, Claro, Escuro e o Automático (seguindo o sistema do usuário).


## 3. Alternativa Descartada

**Deixar o layout fixo com um tema só e sem adaptação para celular**

  - Por que foi descartada: Ficaria muito ruim de enxergar em lugares com pouca luz e quebraria a tela nos dispositivos móveis do estoque.

## 4. Consequência

### Ganhos Reais:
- **Ergonomia Operacional Multiamplar**: Suporte a diferentes turnos e ambientes físicos de trabalho com alternância imediata de contraste e luminosidade.
- **Eficiência e Performance**: Zero overhead no banco de dados e zero requisições HTTP adicionais para persistência de tema.
- **Navegação Intuitiva e Sem Quebras**: Eliminação de barras de rolagem horizontal espúrias e agrupamento coerente de módulos na página principal.

### Custos e Limitações Assumidas:
- **Dependência de Armazenamento Local no Navegador**: Caso o operador limpe o cache e o armazenamento local do navegador, o tema reverte para o modo Padrão/Sistema até nova seleção.

## 5. Commit

- **Hash de Temas Visuais (Dark/Light/Sistema)**: `5dedfaa` — `feat(ui): adiciona suporte a 4 temas (padrao, claro, escuro e sistema) com persistencia local`.
- **Hash de Remodelagem da Home em Grid e Navbar**: `a4b7c89` — `feat(ui): ordenar navbar sequencial pós-logs e reestruturar layout da home em grid 4x2`.
- **Hash de Responsividade e Correção de Overflow**: `2a6a90a` — `fix(ui): ajusta responsividade da navbar e elimina overflow horizontal`.

