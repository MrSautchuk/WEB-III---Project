# ADR 009 — Modelagem de Kits e Anúncios Comerciais: Relacionamento N:M com Entidade Associativa (Lista de Componentes de um Nível), e não Composite GoF Recursivo

> **Declaração de Integridade Acadêmica:** Este conteúdo foi produzido com auxílio de IA.

> **Revisão (v2):** reclassificação conceitual após a arguição do Marco 1. Esta versão substitui a v1, intitulada *"Padrão Estrutural Composite e Modelagem de Kits de Produtos vs. Anúncios Comerciais Desacoplados"*. **A implementação não foi alterada**: mudaram a nomenclatura e a fundamentação. O texto original da decisão (v1) está preservado na seção 1.2.

## 1. Contexto

### 1.1. Contexto de negócio (mantido da v1)

No comércio eletrônico, existe uma divergência conceitual fundamental entre o **Inventário Físico do Catálogo** e a **Estratégia Comercial de Anúncios nos Marketplaces**:
- No catálogo do armazém, o lojista controla produtos individuais pelo SKU físico (ex.: Camiseta Branca Tam M, Cerveja Artesanal IPA 500ml).
- Nos marketplaces, o mesmo produto físico pode ser anunciado de múltiplas maneiras simultâneas:
  1. Anúncio individual clássico (1 unidade).
  2. Kit promocional com multiplicador de quantidade (ex.: "Kit 3 Camisetas Brancas").
  3. Combo composto heterogêneo (ex.: "Kit Churrasco: 1 Avental + 1 Faca de Churrasco + 1 Tábua de Madeira").
  4. Anúncio com benefícios distintos de frete (Anúncio Clássico vs. Anúncio Premium com frete grátis para o mesmo item físico).

Se o sistema adotasse uma modelagem ingênua de 1:1 onde cada `Anuncio` fosse apenas uma cópia direta de um `Produto`, seria impossível vender kits e combos sem duplicar o estoque de forma fictícia, gerando risco fatal de vender o mesmo produto físico duas vezes em anúncios diferentes (*overselling*).

### 1.2. Histórico de evolução do entendimento

| Versão | Como a estrutura foi classificada | Situação |
|---|---|---|
| **v1** (ADR original) | "Padrão estrutural **Composite**" desacoplando `Anuncio` e `Produto` por meio de `AnuncioComposicao`. | Superada quanto ao **nome** do padrão. A implementação foi mantida. |
| **v1.1** (preparação da defesa) | "**Composite plano de dois níveis**": `Anuncio` como composto e `Produto` como folha, sem recursão. | Superada. |
| **v2** (este ADR) | **Relacionamento N:M com entidade associativa** (lista de componentes de um nível, *Bill of Materials* no sentido de modelagem de dados). O Composite GoF recursivo passa a constar como **alternativa descartada por simplicidade**. | **Vigente.** |

**Arguição do Marco 1.** O professor perguntou se, no ADR 009, um kit pode conter outro kit, observando que, se não pode, a estrutura é uma boa tabela N:M com quantidade, e não um Composite recursivo.

**Reanálise.** A equipe conferiu os models `apps/anuncios/models.py` e `apps/catalogo/models.py` contra os requisitos estruturais do Composite descritos pelo GoF (Gamma et al., 1994):

| Requisito do Composite (GoF) | O que os models mostram | Atende? |
|---|---|---|
| Hierarquia parte-todo em árvore | Altura fixa em 1: `Anuncio` → `AnuncioComposicao` → `Produto`. | Não |
| Interface comum (*Component*) que permite tratar folha e composto de modo uniforme | `Anuncio` (domínio comercial) e `Produto` (domínio físico) são modelos independentes, sem base ou interface comum. A cota é calculada apenas no `Anuncio`. | Não |
| Composição recursiva (composto contendo composto) | A FK `AnuncioComposicao.produto` aponta para `Produto`, que não possui componentes. Não há FK autorreferente, e um `Anuncio` não contém outro `Anuncio`. | Não, por construção |

**Conclusão da reanálise.** Um kit **não** contém outro kit. A estrutura implementada é um relacionamento N:M entre `Anuncio` e `Produto`, materializado por uma entidade associativa com atributo (`quantidade`). Não satisfaz os requisitos estruturais do Composite, e chamá-la assim usava o nome do padrão de forma ampla. O próprio docstring de `AnuncioComposicao` já descreve a classe como *"Ficha Técnica / Bill of Materials"*, de modo que esta revisão alinha o texto do ADR ao vocabulário do código.

**Argumento revisto.** A v1 e a preparação da defesa sustentavam que a estrutura plana evitava a "explosão de SKUs fantasmas/virtuais". A reanálise mostrou que esse benefício vem de a composição apontar para **produtos físicos reais**, e não de a estrutura ser plana. Portanto, ele vale **igualmente** para um Composite recursivo, e não distingue as duas opções. O critério de escolha entre elas é a **simplicidade** (seção 3, Alternativa 3).

<details>
<summary><strong>Texto original da Decisão (v1), preservado como registro histórico</strong></summary>

> A equipe decidiu implementar o padrão estrutural **Composite** desacoplando o modelo comercial de `Anuncio` do modelo físico de `Produto` através de uma entidade de composição de primeira classe (`apps/anuncios/models.py: AnuncioComposicao`):
>
> 1. **Entidade Comercial (`Anuncio`)**:
>    - Representa a publicação no marketplace (título, preço comercial de venda, permalink externo, status no canal e cota publicada).
>    - Possui identificador externo `item_id_externo` (ex.: `MLB123456789`).
> 2. **Entidade Fisiológica de Composição (`AnuncioComposicao`)**:
>    - Tabela intermediária de relacionamento N:M com atributos ricos: `anuncio`, `produto` e `quantidade` (multiplicador).
>    - Um anúncio simples possui 1 composição com quantidade = 1.
>    - Um kit possui 1 ou mais composições com multiplicador ≥ 1.
> 3. **Cálculo Dinâmico de Cota Disponível (Algoritmo de Gargalo / *Bottleneck*)**:
>    - O estoque publicado de um anúncio é calculado dinamicamente em tempo de execução:
>
>      $$\text{Cota do Anúncio} = \min_{i \in \text{Composições}} \left( \left\lfloor \frac{\text{Estoque Físico}(P_i)}{\text{Multiplicador}_i} \right\rfloor \right)$$
>
>    - Se o lojista possui 10 cervejas e o anúncio é um "Kit com 3 cervejas", a cota máxima calculada é $\lfloor 10 / 3 \rfloor = 3$ kits.
> 4. **Baixa Proporcional e Blindagem de Deleção**:
>    - A venda de 1 unidade do kit debita atômica e proporcionalmente a quantidade exata de cada produto físico componente (`quantidade_vendida * multiplicador`).
>    - Implementação de proteção contra deleção acidental de vínculos com auditoria baseada em snapshots (`fix/blindagem-de-erro-por-delecao-incorreta`).

</details>

## 2. Decisão

A equipe **mantém a modelagem implementada** e a classifica corretamente: o vínculo entre anúncios comerciais e produtos físicos é um **relacionamento N:M com entidade associativa** (`apps/anuncios/models.py: AnuncioComposicao`), que funciona como **lista de componentes de um nível**. O termo *Bill of Materials* é usado aqui no sentido de modelagem de dados (pai, componente, quantidade por pai), e não no de manufatura. A estrutura **não é** um Composite GoF.

![Correção do ADR 009: de "Composite" para relacionamento N:M (Bill of Materials)](img/adr-009-correcao-tabela-n-m-bom.jpg)

*Figura 1 — Mapeamento relacional N:M entre `Anuncio` e `Produto` por meio de `AnuncioComposicao` (à esquerda) e comparação de topologias: árvore recursiva vs. lista de componentes de um nível (à direita).*

1. **Entidade Comercial (`Anuncio`)** *(mantida da v1)*:
   - Representa a publicação no marketplace (título, preço comercial de venda, permalink externo, status no canal e cota publicada).
   - Possui identificador externo `item_id_externo` (ex.: `MLB123456789`), único dentro da conta (`unique_together = ('conta', 'item_id_externo')`).
2. **Entidade Associativa (`AnuncioComposicao`)**:
   - Relaciona `Anuncio` e `Produto` (FKs `anuncio` e `produto`) e carrega o atributo próprio da relação: `quantidade` (multiplicador do kit). Por isso é uma entidade associativa, e não apenas uma tabela de junção.
   - Um anúncio simples possui 1 composição com quantidade = 1. Um kit possui 1 ou mais composições com multiplicador ≥ 1, por regra de negócio.
   - A navegação reversa usa `related_name='itens_composicao'` (a partir do anúncio) e `related_query_name='composicoes'` (nas consultas), por exemplo `Anuncio.objects.filter(composicoes__produto=instance)`.
3. **Invariantes do modelo**:
   - **Unicidade por par:** `unique_together = ('anuncio', 'produto')`. É uma **regra de domínio imposta pela tabela**: o multiplicador já expressa a multiplicidade ("2 botas" é uma linha com `quantidade = 2`, e não duas linhas). Como o Django não impõe essa unicidade em modelos `through` explícitos, ela é declarada de forma deliberada.
   - **Altura fixa em 1:** `Produto` não possui componentes e `Anuncio` não contém `Anuncio`.
   - **Isolamento de tenant:** `clean()` exige que o produto e a conta do anúncio pertençam à mesma loja.
4. **Tipologia comercial** derivada da composição: *Sem Vínculo*, *Item Simples* (1 produto, multiplicador = 1), *Kit Homogêneo* (1 produto, multiplicador > 1) e *Combo Multi-Produto* (2 ou mais produtos distintos).
5. **Cálculo Dinâmico de Cota Disponível (Algoritmo de Gargalo / *Bottleneck*)** *(mantido da v1)*:
   - $$\text{Cota do Anúncio} = \min_{i \in \text{Composições}} \left( \left\lfloor \frac{\text{Estoque Físico}(P_i)}{\text{Multiplicador}_i} \right\rfloor \right)$$
   - Se o lojista possui 10 cervejas e o anúncio é um "Kit com 3 cervejas", a cota máxima é $\lfloor 10 / 3 \rfloor = 3$ kits.
   - A fórmula pressupõe **uma linha por produto**, o que a unicidade do item 3 garante.
6. **Baixa Proporcional e Blindagem de Deleção** *(mantidas da v1)*:
   - A venda de 1 unidade do kit debita atômica e proporcionalmente a quantidade exata de cada produto físico componente (`quantidade_vendida * multiplicador`).
   - Proteção contra deleção acidental de vínculos, com auditoria baseada em snapshots (`fix/blindagem-de-erro-por-delecao-incorreta`).

## 3. Alternativas Descartadas

A equipe avaliou e **rejeitou formalmente três alternativas de modelagem**. As duas primeiras foram mantidas da v1; a terceira decorre da reanálise.

### Alternativa 1: Acoplamento rígido 1:1 entre Produto e Anúncio (ForeignKey direta única) *(mantida da v1)*
- **Por que foi descartada**: se a tabela `Anuncio` tivesse apenas uma coluna `produto_id` direta simples:
  - O lojista estaria proibido de criar kits ou combos no marketplace.
  - Para criar um anúncio de "Kit 3 Camisetas", o lojista seria forçado a cadastrar um produto falso no catálogo chamado "Kit 3 Camisetas" e dividir manualmente o estoque físico entre a camiseta avulsa e o kit. Isso causaria descompasso imediato: se as camisetas avulsas esgotassem, o sistema não saberia que o kit também deveria ser zerado, resultando em venda sem estoque.

### Alternativa 2: Modelagem de kits apenas como strings/JSON em campos não-relacionais *(mantida da v1)*
- **Por que foi descartada**: armazenar a composição dentro de um campo de texto ou de um `JSONField` no anúncio destrói a integridade referencial do banco relacional. Seria impossível executar consultas SQL indexadas reversas (ex.: *"quais anúncios precisam ser atualizados quando o produto SKU-100 mudar de estoque?"*). O Django ORM exigiria deserializar o JSON de todos os anúncios da loja em memória Python. A tabela relacional `AnuncioComposicao` permite essas consultas por chave estrangeira indexada (`Anuncio.objects.filter(composicoes__produto=instance)`).

### Alternativa 3: Composite GoF recursivo (kits que contêm kits) *(nova na v2)*
- **O que seria**: uma interface comum (*Component*) implementada por produtos físicos (*Leaf*) e por kits (*Composite*), com kits podendo conter outros kits, por exemplo por meio de uma FK autorreferente.
- **Por que NÃO foi descartada por "SKUs fantasmas"**: um Composite recursivo também compõe produtos físicos reais e, portanto, também evita a explosão de SKUs virtuais. Esse argumento, usado na v1 e na preparação da defesa, **não** distingue as duas estruturas.
- **Por que foi descartada: simplicidade.**
  - **Sem requisito de aninhamento.** Os quatro cenários comerciais levantados (seção 1.1) cabem em um único nível.
  - **Mesma expressividade sobre o estoque.** Qualquer kit aninhado pode ser expresso em um nível multiplicando as quantidades ao longo do caminho até os produtos físicos, somando-as quando o mesmo produto aparece em mais de um ramo. A recursão só acrescentaria o **reuso da definição de sub-kits**, que não é requisito atual.
  - **Custo adicional da recursão.** Expansão recursiva no cálculo de cota, detecção de ciclos, limite de profundidade, consulta reversa recursiva (CTE ou iteração em Python) e uma interface uniforme entre `Anuncio` e `Produto`, que hoje são conceitos de domínios distintos (comercial vs. físico).
- **Gatilho de revisão:** se algum marketplace passar a exigir kits aninhados com reuso de sub-kits, a decisão deve ser reavaliada em um novo ADR.

**Referência:** GAMMA, E.; HELM, R.; JOHNSON, R.; VLISSIDES, J. *Design Patterns: Elements of Reusable Object-Oriented Software*. Addison-Wesley, 1994 (padrão Composite).

## 4. Consequência

### Ganhos Reais:
- **Flexibilidade Comercial Ilimitada** *(mantido da v1)*: o lojista pode criar anúncios unitários, kits do mesmo produto ou combos heterogêneos sem duplicar estoque físico.
- **Sincronização Atômica Multicanal** *(mantido da v1)*: uma única venda de kit recalcula e propaga as novas cotas para todos os outros anúncios unitários e kits que compartilham os mesmos componentes.
- **Auditoria e Rastreabilidade Relacional** *(mantido da v1)*: facilidade de auditar, no detalhe do produto, todos os anúncios em que ele está embutido.
- **Simplicidade estrutural:** altura fixa em 1, sem recursão, sem detecção de ciclos e com consulta reversa direta por chave estrangeira.
- **Nomenclatura fiel ao código:** o texto passa a usar o mesmo vocabulário do model (entidade associativa, lista de componentes, *Bill of Materials*).

### Custos e Limitações Assumidas:
- **Complexidade de Recálculo** *(mantida da v1)*: exige cálculo de cotas a cada movimentação de inventário, mitigado pelo isolamento em transações atômicas e por consultas com carregamento antecipado (`select_related` / `prefetch_related`).
- **Sem reuso de sub-kits:** o lojista repete os componentes ao montar kits semelhantes. É a contrapartida direta de não adotar a recursão.
- **Evolução para kits aninhados** exige novo ADR e migração, conforme o gatilho de revisão da seção 3.
- **Terminologia:** o termo *Composite* não deve ser usado para esta estrutura nos demais artefatos (ADRs, README e apresentações).

## 5. Commit

**Implementação (inalterada nesta revisão):**
- **Hash de Publicação de Anúncios e RF-04**: `56d4a7f` — `feat(anuncios): implementa publicacao de anuncios em marketplaces (RF-04)`.
- **Hash de Importação com Suporte a Kits**: `259a925` — `feat(anuncios): finaliza Fase 1 de importacao de anuncios Mercado Livre com suporte a kits e correcao no items/bulk`.
- **Hash de Listagem Reversa de Composições**: `acb7f7f` — `fix(catalogo): corrige listagem de anuncios vinculados via composicao no detalhe do produto`.
- **Hash de Blindagem de Deleção e Snapshots**: `c5981a0` — `fix(anuncios): blindagem de delecao incorreta de composicao, auditoria com snapshots e alerta de produto sem vinculo`.

**Revisão documental (v2):**
- **Branch**: `fix-docs-adr-009-tabela-n-m-nao-composite-gof-recursivo`.
- **Hash da Revisão do ADR 009**: `<hash>` — `docs(adr-009): reclassifica composicao de anuncios como relacionamento N:M (BOM de um nivel), nao Composite GoF recursivo`. *(preencher após o commit)*
