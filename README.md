# Hub Central de Marketplaces

> Projeto desenvolvido na disciplina de Desenvolvimento Web III  
> **FATEC Olímpia** — CST em Desenvolvimento de Software Multiplataforma — 2026/2  
> Professor: Prof. Me. José Ceron

[![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![Django Version](https://img.shields.io/badge/django-5.1-green.svg)](https://www.djangoproject.com/)
[![Test Suite](https://img.shields.io/badge/tests-213%20passed-success.svg)](manage.py)
[![Coverage](https://img.shields.io/badge/coverage-%3E%3D%2040%25-brightgreen.svg)](docs/decisoes.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Taiga Management](https://img.shields.io/badge/scrum-Taiga.io-orange.svg)](https://tree.taiga.io/project/mrsautchuk-http-418/)

---

## Sobre o Projeto

### Problema que Resolve
O comércio eletrônico multicanal impõe grandes desafios financeiros e operacionais para pequenos e médios lojistas. Vendedores frequentemente operam no escuro: sofrem prejuízos com taxas e comissões abusivas ou mal calculadas dos marketplaces (como Mercado Livre, Shopee e Amazon), correm o risco crítico de **ruptura de estoque** (venda de produto esgotado devido à latência de sincronização manual entre plataformas) e ativam campanhas de desconto sem conhecer previamente sua margem de contribuição real.

O **Hub Central de Marketplaces** resolve essa dor ao centralizar a gestão de múltiplos canais em um único painel multi-tenant. O sistema oferece sincronização em tempo real de inventário, integração com APIs oficiais e uma **Calculadora de Viabilidade de Campanhas** que projeta o lucro líquido antes da ativação das promoções, prevenindo surpresas fiscais e garantindo a saúde financeira do vendedor.

### Público-Alvo
- Pequenos e médios lojistas que vendem simultaneamente em múltiplos canais digitais.
- Gestores de e-commerce que necessitam de visão centralizada de pedidos, faturamento e estoque.
- Empreendedores que buscam precificação orientada a dados com margem líquida garantida.

### Organização Parceira
- **Organização / Stakeholder Real:** Projeto de Base Acadêmica / E-commerce Multicanal
- **Contato / Ramo:** Educacional — FATEC Olímpia

---

## Equipe

| Nome Completo | Papel Principal no Scrum | Perfil GitHub |
| :--- | :--- | :--- |
| **Allan M. Sautchuk** | Product Owner / Dev Full-stack | [@MrSautchuk](https://github.com/MrSautchuk) |
| **Oscar Neris** | Scrum Master / Dev Back-end | [@osnrjr](https://github.com/osnrjr) |
| **Guilherme Vilela** | Dev Back-end / APIs | [@guilhermevilela](https://github.com/guilhermevilela) |
| **Rafael Neves** | Dev Front-end / QA | [@rafaelneves](https://github.com/rafaelneves) |
| **Davidson Willis** | Dev Back-end / Integrações | [@davidsonwillis](https://github.com/davidsonwillis) |
| **Vando Souza** | Dev Full-stack / NoSQL | [@vandosouza](https://github.com/vandosouza) |

---

## Tecnologias e Stack

- **Linguagem & Core:** Python 3.12 + Django 5.1
- **API & Autenticação:** Django REST Framework (DRF) + SimpleJWT (Tokens Bearer com RBAC)
- **Documentação de API:** drf-spectacular (Swagger UI / ReDoc / OpenAPI 3.0)
- **Front-end:** Django Templates + TailwindCSS / CSS Moderno + Componentes Interativos
- **Banco de Dados Relacional:** SQLite (desenvolvimento e suíte de testes) / PostgreSQL (ambiente de nuvem)
- **Banco de Dados NoSQL:** MongoDB Atlas (logs analíticos de sincronização e histórico de eventos)
- **Segurança & Criptografia:**
  - Criptografia simétrica Fernet (AES-128 em modo CBC) para tokens OAuth e chaves em repouso
  - Auditoria estática de segredos no CI com Gitleaks
  - Monitoramento contínuo de dependências vulneráveis com Dependabot e pip-audit
- **Qualidade de Código & Testes:**
  - Suíte de 213 testes automatizados (unitários, integração e serviços) com 100% de sucesso
  - pytest + pytest-django + coverage (trava de segurança >= 40%)
  - Linter e formatador de código estático Ruff
- **CI/CD:** GitHub Actions (workflows `ci.yml` e `secret-scan.yml`)
- **Deploy:** Railway / Render / Gunicorn + Whitenoise

---

## Como Rodar Localmente

### Pré-requisitos
- **Python 3.12** instalado na máquina.
- **Git** configurado.
- Gerenciador de pacotes **pip**.

### Passo a Passo

```bash
# 1. Clone o repositório
git clone https://github.com/web3-fatec-olimpia-2026-2/hub_central_marketplace.git
cd hub_central_marketplace

# 2. Crie e ative o ambiente virtual
# No Windows (PowerShell):
python -m venv .venv
.venv\Scripts\Activate.ps1

# No Linux / macOS / WSL:
python3 -m venv .venv
source .venv/bin/activate

# 3. Instale todas as dependências do projeto
pip install --upgrade pip
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente a partir do exemplo oficial
cp .env.example .env
# Edite o arquivo .env preenchendo as chaves conforme necessário

# 5. Aplique as migrações do banco de dados relacional
python manage.py migrate

# 6. Crie um superusuário para acesso ao painel administrativo
python manage.py createsuperuser

# 7. Inicie o servidor de desenvolvimento
python manage.py runserver
```

Acesse a aplicação no navegador em: `http://localhost:8000/`  
Acesse o painel administrativo em: `http://localhost:8000/admin/`

---

## Como Rodar a Suíte de Testes

O projeto possui **213 testes automatizados** cobrindo autenticação, isolamento multi-tenant, integração de contas de marketplace, cálculo de viabilidade e criptografia de credenciais.

```bash
# Executar todos os 213 testes via Django Test Runner
python manage.py test

# Executar via pytest com exibição de cobertura detalhada
pytest --cov=. --cov-report=term-missing

# Gerar relatório HTML de cobertura de código
pytest --cov=. --cov-report=html
# Abra htmlcov/index.html em seu navegador
```

---

## Documentação do Projeto

Toda a documentação técnica, decisões de engenharia e manuais estão organizados na pasta `docs/` e na raiz:

- [Arquitetura do Sistema e Modelo C4](docs/arquitetura.md) — Diagramas de Contexto, Contêineres e Componentes.
- [Catálogo de Requisitos e User Stories](docs/requisitos.md) — Requisitos funcionais, não funcionais e regras de negócio.
- [Decisões Técnicas de Arquitetura (ADRs)](docs/decisoes.md) — Registro histórico das decisões arquiteturais e trade-offs.
- [Manual de Operação e Guia do Usuário](docs/manual-usuario.md) — Instruções ilustradas de uso para o lojista final.
- [Contrato de Colaboração e Contribuição](CONTRIBUTING.md) — Política de branches, regras de PR, matriz Scrum e política de IA.
- [Política de Segurança](SECURITY.md) — Matriz de suporte, reporte responsável de falhas e plano de contenção de incidentes.
- [Licença de Software Livre](LICENSE) — Licença MIT oficial.

---

## Cronograma e Gestão Ágil (Taiga.io)

O projeto é gerenciado sob metodologia ágil Scrum na plataforma **Taiga**:  
👉 **Painel do Projeto:** [https://tree.taiga.io/project/mrsautchuk-http-418/](https://tree.taiga.io/project/mrsautchuk-http-418/)

| Sprint | Período | Objetivo Principal | Status |
| :--- | :--- | :--- | :--- |
| **Sprint 1** | 17/08 - 14/09 | Setup inicial, Django MTV, Modelos Core e CRUD SQLite | Concluído :white_check_mark: |
| **Sprint 2** | 15/09 - 10/10 | Integrações de Marketplace, Mocking e Frontend Interativo | Concluído :white_check_mark: |
| **Sprint 3 (Atual)** | 11/10 - 22/11 | APIs REST, SimpleJWT, 213 Testes, CI/CD e Adequação ao Template Web III | Em Andamento :rocket: |
| **Sprint 4** | 23/11 - 13/12 | Deploy Cloud (PostgreSQL/Nuvem), Polimento Final e Feira de Soluções | Planejado :pushpin: |

---

## Demonstração e Endpoints

- **Ambiente de Homologação / Produção:** [https://hub-central-marketplaces.railway.app](https://hub-central-marketplaces.railway.app)
- **Documentação Interativa da API (Swagger / OpenAPI):** `http://localhost:8000/api/docs/`
- **Vídeo de Demonstração (Screencast / Pitch):** [LINK DO VÍDEO NO YOUTUBE]

---

## Licença

Distribuído sob a licença **MIT**. Consulte o arquivo [LICENSE](LICENSE) para obter mais informações.

---

## Agradecimentos e Reconhecimento

- Ao **Prof. Me. José Ceron**, docente responsável pela disciplina de Desenvolvimento Web III, pelas orientações metodológicas e diretrizes de excelência técnica.
- À **FATEC Olímpia** e ao **Centro Paula Souza** pela infraestrutura e formação profissional orientada ao mercado.
- Aos colegas de turma que colaboraram na revisão por pares e testes cruzados de usabilidade.