# Os códigos foram gerados com auxilio de I.A.
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def run_live_audit():
    session = requests.Session()
    print("=== 1. TESTE DE ROTAS ANÔNIMAS E PROTEÇÃO DE ACESSO ===")
    r_root = session.get(f"{BASE_URL}/", allow_redirects=False)
    print(f"GET / (anônimo) -> Status {r_root.status_code} (Landing Page/Apresentação)")
    assert r_root.status_code == 200, "Raiz anônima deveria carregar landing page (200)"

    r_protected = session.get(f"{BASE_URL}/produtos/", allow_redirects=False)
    print(f"GET /produtos/ (anônimo) -> Status {r_protected.status_code}, Location: {r_protected.headers.get('Location')}")
    assert r_protected.status_code == 302, "Rota protegida deveria redirecionar para login (302)"

    print("\n=== 2. TESTE DE LOGIN E SESSÃO ===")
    r_login_page = session.get(f"{BASE_URL}/auth/login/")
    csrf_token = session.cookies.get('csrftoken')
    print(f"Página de login: Status {r_login_page.status_code}, CSRF Token obtido: {bool(csrf_token)}")
    
    # Login como devmaster
    login_data = {
        'username': 'allan',
        'password': 'admin12345',
        'csrfmiddlewaretoken': csrf_token,
        'next': '/'
    }
    r_login = session.post(f"{BASE_URL}/auth/login/", data=login_data, headers={'Referer': f"{BASE_URL}/auth/login/"})
    print(f"POST /auth/login/ -> Status {r_login.status_code}")

    r_home = session.get(f"{BASE_URL}/")
    print(f"GET / (autenticado como DEV allan) -> Status {r_home.status_code}")
    assert r_home.status_code == 200, "Home deveria carregar 200 para usuário autenticado"

    print("\n=== 3. TESTE DE ROTAS PRINCIPAIS (DEV ROLE) ===")
    endpoints = [
        ("/lojas/", "Gestão de Lojas (Tenants)"),
        ("/usuarios/", "Gestão de Usuários e RBAC"),
        ("/produtos/", "Catálogo de Produtos"),
        ("/categorias/", "Categorias"),
        ("/anuncios/", "Gestão de Anúncios"),
        ("/simulador-promocional/", "Simulador Promocional / Margem"),
        ("/testes/", "Dashboard de Testes de Concorrência"),
        ("/testes/concorrencia/estoque/", "Laboratório Concorrência de Estoque"),
        ("/testes/concorrencia/oauth/", "Laboratório Concorrência de OAuth"),
        ("/mockar-dados/", "Painel de Geração e Expurgo de Mocks"),
        ("/marketplaces/", "Canais e Contas de Marketplace"),
        ("/pedidos/", "Gestão de Pedidos"),
        ("/logs/sincronizacao/", "Logs e Telemetria de Sincronização"),
    ]

    for path, name in endpoints:
        resp = session.get(f"{BASE_URL}{path}")
        print(f"[{resp.status_code}] {name} ({path})")

    print("\n=== 4. TESTE DE SEGURANÇA: RBAC (USUÁRIO COMUM vs ROTAS RESTRITAS) ===")
    # Login como usuário comum da TechZone
    user_session = requests.Session()
    r_lp = user_session.get(f"{BASE_URL}/auth/login/")
    u_csrf = user_session.cookies.get('csrftoken')
    user_login_data = {
        'username': 'user_tech',
        'password': 'senha123',
        'csrfmiddlewaretoken': u_csrf,
        'next': '/'
    }
    r_u_login = user_session.post(f"{BASE_URL}/auth/login/", data=user_login_data, headers={'Referer': f"{BASE_URL}/auth/login/"})
    print(f"Login user_tech (USUARIO): Status {r_u_login.status_code}")

    restricted_endpoints = [
        ("/lojas/", "Criação/Gestão de Lojas (apenas DEV)"),
        ("/lojas/nova/", "Nova Loja (apenas DEV)"),
        ("/testes/", "Laboratório de Concorrência (apenas DEV)"),
        ("/mockar-dados/", "Mockar Dados (apenas DEV)"),
    ]
    for path, name in restricted_endpoints:
        resp = user_session.get(f"{BASE_URL}{path}")
        print(f"Tech_user tentando {name} ({path}) -> Status {resp.status_code} (Esperado: 403 Forbidden)")

    print("\n=== 5. TESTE DE SEGURANÇA: WEBHOOK HMAC E ASSINATURA ===")
    # Teste de webhook sem assinatura válida no endpoint seguro
    r_wh_no_sig = requests.post(
        f"{BASE_URL}/api/v1/webhooks/mercadolivre/",
        data=json.dumps({"topic": "orders_v2", "resource": "/orders/123456"}),
        headers={"Content-Type": "application/json"}
    )
    print(f"POST /api/v1/webhooks/mercadolivre/ sem assinatura -> Status {r_wh_no_sig.status_code} {r_wh_no_sig.text} (Esperado: 401)")

    print("\n=== AUDITORIA DINÂMICA CONCLUÍDA COM SUCESSO ===")

if __name__ == "__main__":
    run_live_audit()
