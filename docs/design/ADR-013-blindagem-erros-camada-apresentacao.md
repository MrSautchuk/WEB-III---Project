# ADR 013 — Blindagem de Erros 

> **Declaração de Integridade Acadêmica:** Este conteúdo foi produzido com auxílio de IA.

## 1. Contexto

 - Em ambientes de produção corporativos, a segurança da aplicação não se restringe apenas ao banco de dados e ao backend. A camada de apresentação exposta ao cliente HTTP frequentemente se torna vetor de vazamento de informações (Information Leakage / Fingerprinting). No Django, quando rotas inexistentes são acessadas ou exceções ocorrem sob depuração indevida, telas padrão revelam a lista completa de rotas (urls.py), versões exatas do framework, caminhos físicos do sistema operacional e configurações internas, facilitando o reconhecimento de alvos por atacantes.

## 2. Decisão

 **Adotar páginas de erro customizadas e blindadas (templates/404.html e templates/500.html)**:
  - Sob DEBUG=False, o sistema renderiza páginas de erro limpas e padronizadas, sem expor nenhuma rota, nome de classe, exceção ou dependência tecnológica.
  - Foram implementados testes automatizados em core/tests.py para validar o comportamento e o status HTTP 404 sanitizado em rotas inexistentes.

## 3. Alternativa Descartada

### Manter as páginas padrão de erro do Django

 - **Por que foi descartada (Justificativa Técnica):** Viola diretamente o OWASP Top 10 A05:2021 (Security Misconfiguration), expondo metadados internos e facilitando técnicas de varredura (fuzzing e mapeamento de diretórios).

## 4. Consequência

 **Ganhos:** Superfície de ataque externa reduzida a zero vazamento de metadados de tecnologia.

 **Custos:** Manutenção dos templates de erro sincronizados com atualizações visuais do hub.

## 5. Commit

 - **Hash de Hardening e Template 404**: `d58cc2e` — `feat(templates): adiciona template customizado templates/404.html e testes`.