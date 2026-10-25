# Os códigos foram gerados com auxilio de I.A.
# Índice Consolidado de Decisões de Arquitetura (ADRs)

> **Disciplina:** Desenvolvimento Web III — FATEC Olímpia (2026/2)  
> **Professor:** Prof. Me. José Ceron  
> **Repositório:** [https://github.com/web3-fatec-olimpia-2026-2/hub_central_marketplace](https://github.com/web3-fatec-olimpia-2026-2/hub_central_marketplace)  
> **Status:** Sprint 3 — Catálogo e Rastreabilidade Arquitetural

---

## 1. Visão Geral das ADRs

Este repositório adota a prática de **Architecture Decision Records (ADRs)** para registrar todas as decisões de design, padrões de projeto (*GoF* e arquiteturais) e trade-offs adotados pela equipe técnica ao longo das sprints.

Os documentos detalhados individuais encontram-se salvos no diretório [`docs/design/`](design/), e a tabela abaixo consolida o índice completo para avaliação docente e auditoria.

---

## 2. Matriz Consolidada de Decisões (ADR-001 a ADR-014)

| Código | Título da Decisão | Padrão / Princípio Envolvido | Problema / Motivação | Decisão Adotada | Documento Completo |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **ADR-001** | Decisão de Projeto e Escopo Base | Monólito Modular (Django MTV + REST) | Definir arquitetura que suporte evolução incremental sem sobrecarga inicial de microserviços. | Adoção do Django 5 com apps desacoplados por bounded context e banco relacional. | [Ver ADR-001](design/ADR-001-decisao-de-projeto.md) |
| **ADR-002** | Validação de Regras de Negócio na Camada de Domínio | Domain Service / Fat Models vs Clean Services | Centralizar lógicas de cálculo de taxas e comissões impedindo regras espalhadas em controllers. | Criação de serviços especializados de domínio em `services.py`, mantendo views focadas em HTTP. | [Ver ADR-002](design/ADR-002-validacao-regras-de-negocio.md) |
| **ADR-003** | Isolamento Estrito Multi-Tenant e RBAC | Shared Database with Discriminator Column (Loja) | Garantir que múltiplos lojistas utilizem a mesma infraestrutura sem risco de vazamento de dados. | Modelo `Loja` com chave estrangeira mandatória em todas as tabelas de negócio e RBAC em 4 papéis. | [Ver ADR-003](design/ADR-003-isolamento-multi-tenant-e-rbac.md) |
| **ADR-004** | Segurança e Criptografia de Credenciais OAuth | Criptografia Simétrica em Repouso (Fernet AES-128) | Proteger chaves de API e tokens de lojistas contra extração em caso de dump acidental de banco. | Implementação de campo customizado cifrado com `cryptography.fernet` via chave `FIELD_ENCRYPTION_KEY`. | [Ver ADR-004](design/ADR-004-seguranca-e-criptografia-de-credenciais-oauth.md) |
| **ADR-005** | Padrão Strategy para Conectores de Marketplaces | **Strategy Pattern (GoF)** | Suportar integração simultânea com Mercado Livre, Shopee e Amazon com contratos intercambiáveis. | Interface abstrata `BaseMarketplaceConnector` com implementações concretas especializadas por canal. | [Ver ADR-005](design/ADR-005-padrao-strategy-para-conectores-de-marketplaces.md) |
| **ADR-006** | Padrão Observer via Django Signals para Estoque | **Observer Pattern (GoF)** | Desacoplar a baixa de estoque da lógica específica de disparo de atualizações para canais externos. | Utilização de `signals` (`post_save`) para notificar os conectores de canais quando o saldo for alterado. | [Ver ADR-006](design/ADR-006-padrao-observer-signals-sincronizacao-estoque.md) |
| **ADR-007** | Circuit Breaker e Trava de Limite (Guardrail) | **Circuit Breaker** + Token Bucket / Rate Limiter | Evitar indisponibilidade em cascata quando a API do Mercado Livre estiver instável ou rate-limited. | Monitoramento de erros com corte temporário de chamadas e guardrail de sincronização em massa. | [Ver ADR-007](design/ADR-007-padrao-circuit-breaker-resiliencia-api.md) |
| **ADR-008** | Idempotência e Transações Atômicas em Webhooks | Transações ACID + Deduplicação por Hash SHA-256 | Retransmissões de rede de webhooks de venda causavam risco de múltiplas baixas de estoque para o mesmo pedido. | Verificação de idempotência no cabeçalho do webhook com bloqueio pessimista (`select_for_update`). | [Ver ADR-008](design/ADR-008-idempotencia-transacoes-atomicas-webhooks.md) |
| **ADR-009** | Modelagem de Anúncios e Kits de Produtos | Modelagem Relacional N:M (Composição de Kits) | Permitir que um anúncio seja composto por múltiplos itens do estoque sem complexidade recursiva desnecessária. | Tabela intermediária de composição N:M mapeando item componente e quantidade, com validação de saldo. | [Ver ADR-009](design/ADR-009-padrao-composite-anuncios-e-kits-produtos.md) |
| **ADR-010** | Motor de Inteligência Financeira e Precificação | Engine de Precificação com Margem Garantida | Lojistas tinham prejuízos ocultos por comissões escalonadas e custos fixos em campanhas promocionais. | Serviço de projeção matemática que bloqueia publicações com margem de contribuição negativa. | [Ver ADR-010](design/ADR-010-motor-inteligencia-financeira-precificacao.md) |
| **ADR-011** | Máquina de Estados e Status Consolidado de Anúncios | **State Pattern (GoF)** / Máquina de Estados | Evitar transições de status inválidas no ciclo de vida de publicações (ex: de rascunho direto para vendido). | Modelagem de transições de estado bem definidas (Rascunho -> Publicado -> Pausado -> Encerrado). | [Ver ADR-011](design/ADR-011-padrao-state-maquina-estados-ciclo-anuncios.md) |
| **ADR-012** | Mock Lab e Modo Híbrido com Feature Flags | Service Mocking / Feature Toggle | Depender de APIs reais nos testes tornava o CI lento, instável e sujeito a limites de quota. | Módulo `mockar_dados` com chave `SIMULAR_ROTAS_MOCK=True` permitindo execução offline dos 213 testes em segundos. | [Ver ADR-012](design/ADR-012-mocking-modo-hibrido-feature-flags.md) |
| **ADR-013** | Segurança Defensiva e Apresentação de Governança | Defense in Depth & Zero Trust Interno | Proteger a aplicação contra vazamento de segredos, ataques de injeção e violações de compliance da FATEC. | Adoção de Gitleaks no CI, Dependabot, auditoria pip-audit e política em 4 níveis para geração de código com IA. | [Ver ADR-013](design/ADR-013-seguranca-defensiva-apresentacao-governanca.md) |
| **ADR-014** | Ergonomia Operacional e Acessibilidade | Design System Acessível (WCAG 2.1) | Proporcionar interface fluida, responsiva e legível para operadores de e-commerce em ambientes de alta carga. | Adoção de paleta com alto contraste, atalhos de teclado, estados de foco evidentes e feedback visual imediato. | [Ver ADR-014](design/ADR-014%20Ergonomia%20Operacional%20e%20Acessibilidade.md) |

---

## 3. Síntese dos Padrões GoF Implementados

- **Criação / Estruturação:**
  - *Strategy Pattern* (`ADR-005`): Conectores intercambiáveis de canais.
  - *Composição / N:M* (`ADR-009`): Gestão de kits de produtos e anúncios agrupados.
- **Comportamentais:**
  - *Observer Pattern* (`ADR-006`): Notificação desacoplada de atualização de estoque via signals.
  - *State Pattern* (`ADR-011`): Máquina de estados para publicações e ciclo de vida de anúncios.
- **Resiliência e Infraestrutura:**
  - *Circuit Breaker* (`ADR-007`): Isolamento de falhas externas.
  - *Idempotent Receiver* (`ADR-008`): Deduplicação de transações em webhooks.
