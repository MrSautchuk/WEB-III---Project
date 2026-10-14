# Os códigos foram gerados com auxilio de I.A.
"""
O QUE FAZ: Suíte de testes do módulo raiz 'hub' (Configurações, Roteamento Global e ASGI/WSGI).
POR QUE FAZ: Garante cobertura de QA para o entrypoint do sistema, verificando resolução das URLs mestres,
             segurança das configurações defensivas e conformidade do roteamento sem gerar overhead.
PERMISSÕES: DEV, ADMIN, SUPERVISOR, USUARIO e anônimos (conforme a rota raiz).
"""

from django.test import TestCase, override_settings
from django.urls import reverse, resolve
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.test.client import RequestFactory


class HubConfiguracoesERotasTestCase(TestCase):
    """
    Testes de integridade das configurações e resolução de rotas globais do Hub.
    Execução ultrarrápida em memória para evitar lentidão ou travamentos.
    """

    def setUp(self):
        self.factory = RequestFactory()

    def test_settings_seguranca_defensiva(self):
        """Valida que configurações essenciais de segurança do Hub estão definidas."""
        self.assertTrue(hasattr(settings, 'SECRET_KEY'))
        self.assertTrue(bool(settings.SECRET_KEY))
        self.assertTrue(hasattr(settings, 'LOGIN_DEBUG'))
        self.assertTrue(hasattr(settings, 'TENANCY_MODE'))
        self.assertIn(settings.TENANCY_MODE, ['single', 'row'])

    def test_resolucao_rotas_principais_sem_travar(self):
        """Valida se as URLs mestres da aplicação resolvem corretamente."""
        # Rota de login
        url_login = reverse('login')
        self.assertEqual(url_login, '/auth/login/')

        # Rota raiz (landing / home)
        match_root = resolve('/')
        self.assertIsNotNone(match_root)

        # Rota do painel de testes de concorrência
        url_testes = reverse('testes_dashboard')
        self.assertEqual(url_testes, '/testes/')

        # Rota de simulação de concorrência de estoque
        url_estoque_conc = reverse('teste_concorrencia_estoque')
        self.assertEqual(url_estoque_conc, '/testes/concorrencia/estoque/')

        # Rota de concorrência OAuth
        url_oauth_conc = reverse('teste_concorrencia_oauth')
        self.assertEqual(url_oauth_conc, '/testes/concorrencia/oauth/')

    def test_wsgi_and_asgi_applications_instantiation(self):
        """Garante que as aplicações WSGI e ASGI são importadas sem erros de bootstrapping."""
        from hub.wsgi import application as wsgi_app
        from hub.asgi import application as asgi_app
        self.assertIsNotNone(wsgi_app)
        self.assertIsNotNone(asgi_app)
