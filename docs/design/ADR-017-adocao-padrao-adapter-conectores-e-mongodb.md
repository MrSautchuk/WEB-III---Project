# ADR 017 — Formalização do Padrão Adapter nos Conectores Externos e MongoDB

- **Data:** 2026-11-22
- **Status:** Em implantação (Semi-implantado — refatoração planejada na Sprint 3)
- **Decisores:** Equipe Hub Central de Marketplaces (Allan, Davidson, Guilherme, Oscar, Rafael, Vando)

> **Declaração de Integridade Acadêmica:** Este conteúdo foi produzido com auxílio de IA.

## Contexto

Na auditoria técnica dos padrões do projeto, identificamos que a tradução de contratos externos incompatíveis já ocorre de maneira **semi-implantada / conceitual** em dois pontos principais:
1. Nos conectores de marketplaces (`apps/marketplaces/connectors/mercadolivre.py`, `shopee.py`, `magalu.py`, `amazon.py`), onde a docstring de `BaseMarketplaceConnector` (`apps/marketplaces/connectors/base.py:16`) e `ContaMarketplace.get_connector` (`apps/marketplaces/models.py:269`) citam `Strategy / Adapter`, mas os conectores executam requisições HTTP (`requests`) e mapeamento de payloads JSON diretamente dentro das estratégias concretas, sem um componente `Adapter` dedicado separando o cliente externo (`Adaptee`) da tradução de contrato.
2. Em `apps/core/mongodb.py` (`get_mongodb_client`, `get_mongodb_database`, `log_audit_event`), que encapsula `pymongo.MongoClient` via funções procedurais em nível de módulo, e em `apps/marketplaces/security_webhook.py` (`validar_assinatura_e_anti_replay`), que normaliza cabeçalhos HMAC de diferentes canais (`x-signature`, `authorization`, `x-hub-signature-256`).

## Decisão

**APLICAMOS / VAMOS FORMALIZAR o padrão Adapter:** o padrão **cabe** para isolar as fronteiras de APIs externas e persistência documental (`pymongo`) e encontra-se **semi-implantado**; decidimos **alterar e refatorar** esses pontos para criar adaptadores dedicados (como `MongoAuditAdapter` e adaptadores de payload/cliente para os conectores externos), separando claramente a estratégia de negócio do contrato de terceiros.

## Justificativa e Alternativa Descartada

- **Por que cabe:** `MercadoLivreConnector` acumula mais de 1.400 linhas misturando protocolo OAuth2, cliente HTTP, retry, mocks e conversão de schemas JSON do Mercado Livre (`price`, `available_quantity`, `listing_type_id`, `/items/bulk`). Isolar um Adapter dedicado reduz o acoplamento ao formato externo de cada API/driver (inclusive do `pymongo`) e facilita testes com dublês em memória.
- **Alternativa descartada:** Manter a tradução misturada dentro das classes Strategy e manter `mongodb.py` apenas como helpers procedurais sem interface comum — descartado porque dificulta trocar clientes HTTP/SDKs de terceiros ou simular o armazenamento NoSQL em testes unitários sem monkeypatch global.
- **Delimitação em Python:** Como Python suporta *duck typing* (`Protocol` / ABCs leves), os adaptadores não precisam de hierarquias burocráticas: basta uma classe Adapter fina recebendo o cliente externo (`Adaptee`) por injeção e expondo o método esperado pelo domínio.

## Consequências

- **Positivas:** Desacoplamento limpo entre o padrão **Strategy** (fluxo do conector no Hub) e o padrão **Adapter** (tradução de APIs externas e driver NoSQL), além de maior testabilidade.
- **Custo / Plano de ação:** Exige refatoração incremental registrada no Taiga (Sprint 3) para extrair os adaptadores de `mercadolivre.py` e `apps/core/mongodb.py` sem quebrar a suíte de testes existente.

## Commit

Rastreável a partir do commit de consolidação do Caderno de Design e da refatoração planejada na Sprint 3 (`main`).
