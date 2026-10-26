# Os códigos foram gerados com auxilio de I.A.
# Catálogo de Requisitos de Software — Hub Central de Marketplaces

> **Disciplina:** Desenvolvimento Web III — FATEC Olímpia (2026/2)  
> **Professor:** Prof. Me. José Ceron  
> **Repositório:** [https://github.com/web3-fatec-olimpia-2026-2/hub_central_marketplace](https://github.com/web3-fatec-olimpia-2026-2/hub_central_marketplace)  
> **Status:** Sprint 3 — Catálogo Consolidado de Requisitos e Regras de Negócio

---

## 1. Introdução e Visão Geral

Este documento detalha o catálogo de Requisitos Funcionais (RFs), Regras de Negócio (RNs) e Requisitos Não-Funcionais (RNFs) do **Hub Central de Marketplaces**. Todos os requisitos foram modelados no formato ágil de *User Stories* e encontram-se rastreados na plataforma de gestão Scrum do projeto no **Taiga.io**.

---

## 2. Requisitos Funcionais (RF)

| ID | Nome do Requisito | User Story (Como / Quero / Para) | Módulo Alvo | Prioridade |
| :--- | :--- | :--- | :--- | :--- |
| **RF-01** | Autenticação e Gestão de Acesso RBAC | **Como** lojista ou administrador, **quero** autenticar via credenciais seguras ou token Bearer JWT e ter acesso restrito conforme meu papel (DEV, ADMIN, SUPERVISOR, USUARIO), **para** garantir que dados sensíveis da loja não sejam expostos a operadores não autorizados. | `apps.accounts` | Essencial (P0) |
| **RF-02** | Governança Multi-Tenant por Loja | **Como** lojista de uma organização, **quero** que todos os meus produtos, pedidos, integrações e relatórios financeiros sejam estritamente isolados da minha loja, **para** impedir qualquer vazamento de dados entre empresas distintas na mesma infraestrutura. | `apps.tenancy` | Essencial (P0) |
| **RF-03** | Catálogo de Produtos e Composição de Kits | **Como** gestor de catálogo, **quero** cadastrar produtos simples, variações de SKU e kits compostos por múltiplos itens, **para** que o estoque dos componentes unitários seja abatido corretamente quando um kit for vendido em um marketplace. | `apps.catalogo` | Alta (P1) |
| **RF-04** | Conexão Segura com Marketplaces | **Como** lojista, **quero** conectar minhas contas de vendedores (Mercado Livre, Shopee, Amazon) autorizando tokens OAuth2 e salvando credenciais com criptografia, **para** permitir a sincronização automatizada sem expor chaves de API. | `apps.marketplaces` | Essencial (P0) |
| **RF-05** | Calculadora e Simulador de Viabilidade | **Como** vendedor multicanal, **quero** simular o preço de venda de um anúncio deduzindo comissões de marketplace, frete e custos fixos/variáveis, **para** identificar a margem líquida real e evitar prejuízos antes de ativar uma campanha. | `apps.financeiro` | Alta (P1) |
| **RF-06** | Gestão e Mapeamento de Anúncios | **Como** lojista, **quero** vincular produtos do meu catálogo local a anúncios específicos em múltiplos marketplaces parceiros, **para** atualizar títulos, preços e status de forma centralizada. | `apps.anuncios` | Alta (P1) |
| **RF-07** | Ingestão e Notificação de Webhooks | **Como** sistema integrado, **quero** receber notificações assíncronas de vendas originadas nos marketplaces e validar sua assinatura HMAC e idempotência, **para** garantir que nenhum pedido seja processado em duplicidade. | `apps.pedidos` | Essencial (P0) |
| **RF-08** | Sincronização e Baixa Atômica de Estoque | **Como** lojista, **quero** que uma venda em qualquer canal reduza imediatamente e atomicamente o estoque local e envie o saldo atualizado para todos os outros canais integrados, **para** prevenir o risco operacional de ruptura de estoque. | `apps.pedidos` / `apps.catalogo` | Essencial (P0) |

---

## 3. Regras de Negócio (RN)

As regras de negócio abaixo representam invariantes e restrições mandatórias do domínio:

### **RN-01: Isolamento Estrito Multi-Tenant**
- Todas as operações de leitura, criação, alteração ou deleção de entidades associadas a uma loja devem filtrar obrigatoriamente pelo identificador da `Loja` vinculada à sessão do usuário logado ou ao token JWT ativo.
- O acesso de um usuário aos dados de outra loja resulta em exceção imediata de permissão (`PermissionDenied`).

### **RN-02: Bloqueio de Precificação com Margem Negativa**
- A calculadora de viabilidade impede a ativação de qualquer anúncio ou campanha promocional cuja margem de contribuição líquida projetada resulte em valor inferior à **Margem Mínima de Segurança** estipulada nas configurações financeiras da loja.
- Caso o usuário tente forçar a publicação, o sistema exige confirmação explícita de exceção com registro em log de auditoria.

### **RN-03: Guardrail de Sincronização em Massa**
- Para mitigar disparos acidentais ou ataques de negação de serviço contra as APIs externas dos marketplaces, a plataforma implementa uma trava de limite (*Guardrail*) que limita alterações simultâneas de estoque/preço a lotes máximos controlados por janela de tempo.
- Falhas consecutivas de comunicação com o parceiro ativam o padrão *Circuit Breaker* (ADR-007), suspendendo temporariamente novas chamadas para evitar penalidades de taxa da API (HTTP 429).

### **RN-04: Concorrência Segura e Lock Pessimista na Baixa de Estoque**
- Quando um webhook de pedido externo ou checkout local é processado, a consulta de verificação de saldo de estoque do produto é executada com bloqueio exclusivo em nível de banco de dados (`select_for_update()`) dentro de uma transação atômica (`transaction.atomic()`).
- Se o saldo for insuficiente, a transação sofre rollback seguro e um alerta de divergência de inventário é gravado para o lojista.

---

## 4. Requisitos Não-Funcionais (RNF)

| ID | Requisito Não-Funcional | Descrição e Métrica de Aceite |
| :--- | :--- | :--- |
| **RNF-01** | **Segurança Criptográfica em Repouso** | Todos os tokens de acesso OAuth2, senhas de aplicação e segredos de webhook salvos no banco de dados devem ser obrigatoriamente criptografados utilizando o algoritmo Fernet (AES-128 em modo CBC com assinatura HMAC-SHA256). |
| **RNF-02** | **Desempenho e Latência de Resposta** | Os endpoints da API REST e as views da aplicação web devem responder a requisições locais em tempo inferior a 200ms sob condições normais de operação. |
| **RNF-03** | **Qualidade e Cobertura Mínima de Testes** | O repositório deve manter cobertura mínima de testes automatizados superior ou igual a **40%**, auditada em cada Pull Request pelo CI (`pytest-cov --cov-fail-under=40`), assegurando não-regressão da suíte de 213 testes. |
| **RNF-04** | **Idempotência no Processamento de Eventos** | A API de recepção de webhooks deve calcular o hash SHA-256 do payload do evento e verificar a existência prévia na tabela de idempotência, garantindo que retransmissões de rede não gerem baixas de estoque duplicadas. |
| **RNF-05** | **Conformidade com Diretrizes FATEC Web III** | O projeto deve obedecer à política pedagógica de IA declarada, manter a suíte de lint com Ruff, e respeitar a matriz de papéis rotativos Scrum no Taiga. |
