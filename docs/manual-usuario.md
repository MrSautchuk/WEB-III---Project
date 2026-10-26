# Os códigos foram gerados com auxilio de I.A.
# Manual de Operação e Guia do Usuário — Hub Central de Marketplaces

> **Disciplina:** Desenvolvimento Web III — FATEC Olímpia (2026/2)  
> **Professor:** Prof. Me. José Ceron  
> **Repositório:** [https://github.com/web3-fatec-olimpia-2026-2/hub_central_marketplace](https://github.com/web3-fatec-olimpia-2026-2/hub_central_marketplace)  
> **Status:** Sprint 3 — Manual Oficial do Lojista e Avaliador

---

## 1. Bem-vindo ao Hub Central de Marketplaces

O **Hub Central de Marketplaces** foi desenvolvido para simplificar e proteger a operação de vendas multicanal do seu e-commerce. A plataforma centraliza estoques de diferentes marketplaces (como Mercado Livre, Shopee e Amazon), automatiza a baixa de inventário em tempo real e calcula a viabilidade financeira de promoções com margem de lucro garantida.

Este manual foi elaborado tanto para o **lojista no dia a dia operacional** quanto para o **docente/avaliador** durante a auditoria acadêmica.

---

## 2. Acesso ao Sistema e Níveis de Permissão (RBAC)

O sistema conta com controle de acesso baseado em papéis (*Role-Based Access Control* - RBAC) organizado em 4 grupos hierárquicos:

| Perfil | Código | Responsabilidades Principais | Acessos Típicos |
| :--- | :--- | :--- | :--- |
| **Desenvolvedor** | `DEV` (Grupo 4) | Acesso irrestrito a todas as configurações de infraestrutura, logs NoSQL e matriz de segurança. | Painel Django Admin, matriz de permissões e Mock Lab. |
| **Administrador** | `ADMIN` (Grupo 3) | Gestão da loja, cadastro de operadores, configuração de contas de marketplace e margens financeiras. | Conexões de API, parâmetros fiscais e relatórios gerenciais. |
| **Supervisor** | `SUPERVISOR` (Grupo 2) | Gestão de catálogo, precificação, simulação de campanhas e acompanhamento de pedidos. | Catálogo, kits, simulador de preços e pedidos. |
| **Operador** | `USUARIO` (Grupo 1) | Consulta de estoque, cadastro de produtos simples e atendimento a pedidos. | Visualização de produtos e baixa manual de inventário. |

### 2.1 Como Efetuar Login
1. Acesse o endereço da aplicação no navegador: `http://localhost:8000/accounts/login/` (ou a URL de produção).
2. Informe seu **Usuário** e **Senha**.
3. Clique em **Entrar**. Se você for o administrador inicial em ambiente local, utilize as credenciais geradas via `python manage.py createsuperuser`.

---

## 3. Gestão de Catálogo e Produtos

### 3.1 Cadastro de Produtos e Categorias
1. No menu lateral, navegue até **Catálogo → Produtos**.
2. Clique no botão **+ Novo Produto**.
3. Preencha os campos obrigatórios:
   - **Nome do Produto**: Título comercial claro.
   - **SKU**: Código identificador único do produto em seu estoque interno.
   - **Categoria**: Selecione a categoria mercadológica correspondente.
   - **Custo de Aquisição (R$)**: Valor pago pelo item junto ao fornecedor (base para o simulador de margens).
   - **Estoque Inicial**: Saldo disponível para venda física.
4. Clique em **Salvar**. O produto estará pronto para precificação e publicação em anúncios.

### 3.2 Composição de Kits de Produtos
O Hub permite vender pacotes agrupados (ex: *Kit 3 Camisetas*) sem duplicar estoque físico:
1. Acesse **Catálogo → Kits**.
2. Clique em **Criar Novo Kit**.
3. Adicione os produtos componentes e suas respectivas quantidades unitárias (ex: 2x Produto A + 1x Produto B).
4. O sistema calculará automaticamente o estoque máximo comercializável do kit com base no componente de menor saldo (*gargalo de estoque*).

---

## 4. Conexão com Marketplaces e Laboratório de Homologação (Mock Lab)

### 4.1 Conectando uma Conta do Mercado Livre
1. Acesse **Marketplaces → Conexões**.
2. Clique em **Conectar Mercado Livre**.
3. Você será redirecionado para o fluxo oficial de autorização OAuth2 da plataforma parceira.
4. Ao autorizar, o Hub armazena o token de acesso de forma criptografada em repouso (Fernet AES-128).

### 4.2 Chaveamento de Modo Simulado (Mock Lab)
Para fins de avaliação docente, testes acadêmicos ou trabalho offline sem depender de contas reais com saldo:
1. No arquivo `.env`, certifique-se de que a variável `SIMULAR_ROTAS_MOCK=True` está ativa.
2. Acesse o menu **Homologação / Mock Lab**.
3. Neste painel, o avaliador pode:
   - Simular resposta instantânea da API do Mercado Livre.
   - Disparar um webhook falso de pedido aprovado com payload assinado.
   - Observar a baixa atômica de estoque em tempo real na tela sem gastar dinheiro real.

---

## 5. Motor de Precificação e Simulador de Viabilidade de Campanhas

Um dos grandes diferenciais do Hub é a prevenção contra prejuízos em promoções agressivas:

### 5.1 Como Simular a Viabilidade de um Anúncio
1. Acesse **Financeiro → Simulador de Preços**.
2. Selecione o **Produto** ou **Kit** que deseja anunciar.
3. Escolha o **Marketplace Alvo** (ex: Mercado Livre Clássico ou Premium).
4. O sistema carrega automaticamente:
   - O custo base do produto.
   - A alíquota de comissão percentual do canal (ex: 12% ou 16%).
   - A taxa fixa por item e estimativa de frete grátis.
5. Digite o **Preço de Venda Pretendido** ou a **Margem Líquida Alvo (%)**.
6. O **Simulador** projeta em tempo real:
   - Valor bruto da venda.
   - Total de comissões e tarifas descontadas pelo canal.
   - Lucro líquido em Reais (R$) e margem percentual líquida.
7. **Regra de Proteção (RN-02):** Se a margem calculada for inferior à margem de segurança configurada pela loja, o botão de publicação é **bloqueado**, exibindo um aviso em destaque para evitar prejuízos acidentais.

---

## 6. Sincronização e Baixa Atômica de Pedidos

1. **Recepção Automática:** Quando um cliente compra em qualquer marketplace, a notificação de venda chega ao endpoint de webhook `/api/v1/marketplaces/webhook/`.
2. **Idempotência:** O sistema valida o hash do evento, impedindo que a mesma venda seja processada duas vezes em caso de retransmissão de rede.
3. **Baixa Atômica:** O saldo de estoque é reduzido com lock pessimista em banco de dados (`select_for_update()`).
4. **Broadcast de Estoque:** Automaticamente, o Hub dispara o novo saldo para todos os outros canais conectados, evitando o risco de ruptura de estoque (*overselling*).

---

## 7. Solução de Problemas Frequentes (FAQ)

- **Minha sincronização retornou alerta de limite de taxa (HTTP 429)?**  
  *Solução:* O mecanismo de *Circuit Breaker* (ADR-007) atuará pausando requisições temporariamente para proteger sua reputação na API parceira. Aguarde alguns minutos ou reduza o tamanho do lote de sincronização.
- **Como restauro o acesso de um operador com senha esquecida?**  
  *Solução:* O usuário pode clicar no link "Esqueci minha senha" na tela de login ou o administrador (`ADMIN`/`DEV`) pode redefinir o acesso via painel administrativo.
