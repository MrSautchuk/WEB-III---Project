# ADR 019 — Decisão de Não Adoção do Padrão Decorator (GoF) e Delimitação em Python

- **Data:** 2026-11-22
- **Status:** Aceito (Não aplicamos — fecha o catálogo de padrões de ILP-037)
- **Decisores:** Equipe Hub Central de Marketplaces (Allan, Davidson, Guilherme, Oscar, Rafael, Vando)

> **Declaração de Integridade Acadêmica:** Este conteúdo foi produzido com auxílio de IA.

## Contexto

Para o fechamento do catálogo de padrões de projeto do semestre (`Homework 10c` — ILP-037), analisamos o código do Hub Central de Marketplaces (`apps/marketplaces/connectors/mercadolivre.py`, `apps/financeiro/services.py`, `apps/accounts/rbac.py`, `apps/tenancy/permissions.py`) para avaliar se caberia aplicar o padrão estrutural **Decorator (GoF)** — por exemplo, para empilhar comportamentos opcionais em tempo de execução sobre conectores (retry, log, interceptação de mock) ou sobre cálculos de preço/taxas.

## Decisão

**NÃO APLICAMOS o padrão estrutural Decorator (GoF)** no código do projeto.

## Justificativa, Alternativa Descartada e Delimitação em Python

O padrão **Decorator (GoF) cabe** conceitualmente quando há combinações dinâmicas e empilháveis de responsabilidades opcionais em tempo de execução mantendo a mesma interface do componente base. Contudo, decidimos **ainda não implantar** pois o projeto já atende aos requisitos utilizando **recursos nativos do Python e do Django** que estão funcionando de forma clara e simples:

1. **Preocupações transversais (auth, permissões, transações, signals):** São tratadas nativamente por **funções decoradoras de sintaxe `@` do Python** (`@property`, `@classmethod`, `@transaction.atomic`, `@receiver`, `@require_GET`, `require_funcionalidade` em `apps/accounts/rbac.py`, `dev_required` em `apps/tenancy/permissions.py`), **Mixins estáticos de CBV** (`ModuloRequeridoMixin`, `FinancialAccessMixin`, `SyncPermissionMixin`) e **Middlewares Django**.
2. **Cálculo de taxas/preço (`SimuladorPromocionalService`):** As variações de tarifa são **fixas/parametrizadas por banco** (`ConfiguracaoTaxasLoja` e `ParametroCanalMarketplace`), onde soma direta sobre lista/parâmetros resolve sem necessidade de empilhar classes `Decorator` (evitando cerimônia desnecessária).
3. **Conectores (`MercadoLivreConnector`):** Retry e logs são hoje pontuais e previsíveis dentro do método `request`, sem combinação arbitrária de wrappers em runtime.

- **Alternativa descartada:** Criar classes wrapper GoF (ex.: `LoggingConnectorDecorator(RetryConnectorDecorator(MercadoLivreConnector))`) quando as necessidades atuais já são atendidas por funções auxiliares, Middlewares e Mixins nativos do Django sem ganhos proporcionais à complexidade extra.
- **Delimitação obrigatória em Python:** A **sintaxe `@decorator` do Python** (como `@login_required`, `@property`, `@receiver` e `require_funcionalidade`) é um recurso da linguagem (funções de ordem superior / descritores em tempo de definição) e **não se confunde** com o **padrão estrutural Decorator do GoF** (que envolve composição de objetos em runtime implementando a mesma interface `Component` para empilhar comportamentos). Da mesma forma, somas fixas de taxas ou extras usam lista/parâmetros simples, não Decorator.

## Consequências

- **Positivas:** Código idiomático em Python/Django, sem hierarquias extras de wrappers nem confusão entre recursos da linguagem e padrão GoF.
- **Limitações assumidas:** Caso futuramente os conectores precisem compor dinamicamente múltiplos pipelines opcionais por conta (ex.: cache + rate-limiter + mock + telemetria configuráveis por tenant em runtime), o padrão Decorator GoF poderá ser reavaliado sobre `BaseMarketplaceConnector`.

## Commit

Rastreável a partir do commit de consolidação do Caderno de Design (Sprint 3) na branch `main`.
