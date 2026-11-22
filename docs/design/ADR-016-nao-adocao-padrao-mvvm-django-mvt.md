# ADR 016 — Decisão de Não Adoção do Padrão MVVM (Uso Nativo de Django MVT)

- **Data:** 2026-11-22
- **Status:** Aceito (Não aplicamos)
- **Decisores:** Equipe Hub Central de Marketplaces (Allan, Davidson, Guilherme, Oscar, Rafael, Vando)

> **Declaração de Integridade Acadêmica:** Este conteúdo foi produzido com auxílio de IA.

## Contexto

Na camada de apresentação do projeto (`apps/*/views.py`, `apps/site/context_processors.py`, `templates/`), avaliamos se valeria a pena introduzir uma camada formal de **ViewModel** (padrão **MVVM — Model-View-ViewModel**) para isolar decisões de exibição (formatação, rótulos condicionais, estados derivados e estado de tela no cliente).

Atualmente, a interface utiliza Django MVT (`ListView`, `DetailView`, `FormView`, `TemplateView`), Context Processors globais (`apps/site/context_processors.py` e `apps/tenancy/context_processors.py`), HTMX para fragmentos parciais (`templates/catalogo/_produto_tabela.html`), manipulação DOM pontual em `static/js/app.js` / `templates/financeiro/simulador_promocional.html` e apenas um toggle local com Alpine.js em `templates/catalogo/produto_list.html` (`x-data="{ filtrosAbertos: false }"`).

## Decisão

**NÃO APLICAMOS o padrão MVVM** (nem classes `ViewModel` dedicadas no back-end, nem estado reativo MVVM completo em SPA no front-end).

## Justificativa e Alternativa Descartada

O padrão **MVVM cabe** em aplicações com estado complexo e reatividade bidirecional intensa no navegador (ex.: SPAs React/Vue/Angular) ou em telas desktop/mobile desacopladas do servidor. Porém, decidimos **ainda não implantar** pois o sistema utiliza ferramentas nativas do **Django (MVT + Django Forms + Template Tags + Context Processors + HTMX)** que atendem plenamente às necessidades atuais sem duplicar modelos de estado entre back-end e front-end.

- **Alternativa descartada:** Criar classes `*ViewModel` em Python embrulhando cada `Model`/`Service` ou migrar templates para estado client-side com `x-model` / JSON serializers dedicados apenas para renderização HTML. Isso duplicaria mapeamentos que o `ModelForm`, as CBVs e os templates do Django já resolvem nativamente com menos código e menor acoplamento.
- **Delimitação em Python/Django:** No ecossistema Django MVT, regras de negócio ficam na **Service Layer** (`services.py`), enquanto formatação leve de exibição fica em `@property` de apoio, `context_processors.py` e `templatetags`. Um `ViewModel` formal só se justificaria se o mesmo payload precisasse alimentar múltiplos clientes ricos independentes com lógica de apresentação complexa e não trivial.

## Consequências

- **Positivas:** Menor número de camadas intermediárias, manutenção simples dos templates Django + HTMX e zero duplicação de estado entre servidor e cliente.
- **Limitações assumidas:** Caso o front-end evolua futuramente para uma SPA desacoplada via API REST (DRF), os serializers e viewsets deverão assumir o contrato de dados que hoje é montado nos contextos das CBVs.

## Commit

Rastreável a partir do commit de consolidação do Caderno de Design (Sprint 3) na branch `main`.
