# ADR 014 — Conformidade Acadêmica e Governança de Código (Uso Nível 2 de IA)

> **Declaração de Integridade Acadêmica:** Este conteúdo foi produzido com auxílio de IA.

## 1. Contexto

Para cumprir as regras da disciplina ILP-037 do professor José Ceron Neto na FATEC, o uso de inteligência artificial é permitido no Nível 2. Como o código-fonte do projeto foi amplamente acelerado e estruturado com auxílio de IA, a equipe precisava definir uma estratégia de rastreabilidade e transparência acadêmica sem comprometer a limpeza e a legibilidade do código.

## 2. Decisão

 **Cabeçalho Global de Atribuição por Arquivo**:
   - Em vez de anotações dispersas ou inseridas linha a linha, adotamos a inclusão padronizada de um único cabeçalho de conformidade acadêmica no topo de todos os arquivos de código-fonte (.py) do projeto:

     ```python
     # Os códigos foram gerados com auxilio de I.A.
     ```
   - Esse padrão atende à diretriz de autoria híbrida da FATEC de forma limpa, concentrando a declaração institucional onde ela é visível a qualquer auditor sem impactar o escopo funcional das classes e funções.

## 3. Alternativa Descartada

 **Inserir comentários ou tags de IA linha a linha no código**
  - Poluiria excessivamente a base de código (code pollution), dificultando a leitura, a manutenção e a refatoração dos scripts em Python. A padronização em cabeçalho único resolve a governança acadêmica mantendo o código limpo e organizado.

## 4. Consequência

### Ganhos Reais:
- **Limpeza de Código (Clean Code)**: Evita a poluição visual gerada por múltiplos comentários repetitivos ao longo das funções e métodos.
- **Total Conformidade Normativa com a FATEC**: Alinhamento estrito com os requisitos éticos estabelecidos pelo Prof. José Ceron Neto para a disciplina ILP-037.
- **Rastreabilidade e Governança**: Transparência profissional evidenciando o uso da IA como acelerador de produtividade, garantindo que a equipe mantenha o domínio técnico sobre o que foi gerado.

### Custos e Limitações Assumidas:
- **Disciplina Contínua de Versionamento**: Exigência de atenção da equipe para garantir que todo novo arquivo .py gerado receba o cabeçalho obrigatório antes de ir para o repositório.

## 5. Commit

- **Hash de Governança de Cabeçalho de IA:** `7aa267f` — `fix(code-standard): introduz cabecalho obrigatorio de atribuicao de I.A. nos arquivos fontes`