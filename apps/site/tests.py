# Os códigos foram gerados com auxilio de I.A.
"""
O QUE FAZ: Suíte de testes automatizados de segurança, contraste WCAG 2.1, prevenção de CSS Injection e chaveamento de visibilidade pública (Doc ① §22.1 itens 13, 14, 17 e §11.1).
POR QUE FAZ: Garante que as proteções arquiteturais e contratos visuais do ecossistema Django funcionem sem regressões.
"""

from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from .models import ConfigTema, ConfigSite
from .utils_tema import (
    calcular_razao_contraste, validar_cor_hex, validar_contraste_wcag,
    gerar_css_tema, PRESETS_MODELOS
)
from apps.tenancy.models import Loja, PerfilUsuario, PapelUsuarioEnum


class TemaContrasteESegurancaTests(TestCase):
    """Validações de contraste WCAG 2.1 e blindagem contra injeção de CSS (Doc ① §22.1 item 13)."""

    def test_presets_canonicos_possuem_contraste_valido(self):
        """Todos os 10 modelos canônicos (T01 a T10) devem cumprir WCAG 2.1 estrito."""
        for modelo_id, p in PRESETS_MODELOS.items():
            with self.subTest(modelo=modelo_id):
                # Não deve levantar ValidationError
                try:
                    validar_contraste_wcag(
                        cor_fundos=p['fundos'],
                        cor_destaques=p['destaques'],
                        cor_escritas=p['escritas'],
                        modelo=modelo_id
                    )
                except ValidationError as e:
                    self.fail(f"Modelo {modelo_id} reprovou no teste de contraste: {e}")

    def test_contraste_insuficiente_lanca_validation_error(self):
        """Cores com contraste abaixo de 4.5:1 (escritas) ou 3:1 (destaques) devem ser bloqueadas."""
        # Cinza claro sobre branco resulta em contraste muito baixo (~1.5:1)
        fundo_branco = "#FFFFFF"
        cinza_muito_claro = "#DDDDDD"

        with self.assertRaises(ValidationError) as ctx:
            validar_contraste_wcag(
                cor_fundos=fundo_branco,
                cor_destaques=cinza_muito_claro,
                cor_escritas=cinza_muito_claro,
                modelo='T05'
            )
        self.assertIn('cor_escritas', ctx.exception.message_dict)

    def test_rejeicao_estrita_de_css_injection(self):
        """Valores que tentam injetar regras CSS arbitrárias devem ser sumariamente rejeitados."""
        payloads_maliciosos = [
            "#FFF; background: url('https://evil.com/leak');",
            "red; } body { display: none; } /*",
            "#123456; color: red;",
            "<script>alert(1)</script>",
            "#GGGGGG",
            "rgb(0,0,0)",
            "transparent",
        ]

        for payload in payloads_maliciosos:
            with self.subTest(payload=payload):
                with self.assertRaises(ValidationError):
                    validar_cor_hex(payload, "cor_teste")

    def test_endpoint_tema_css_retorna_200_e_content_type_correto(self):
        """A rota /tema.css deve ser pública, retornar 200, text/css e headers de cache (Doc ① §22.1 item 14)."""
        response = self.client.get(reverse('site:tema_css'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response['Content-Type'].startswith('text/css'))
        self.assertIn('max-age=31536000', response.get('Cache-Control', ''))
        self.assertIn('--tema-fundo:', response.content.decode('utf-8'))
        self.assertIn('.btn-primary', response.content.decode('utf-8'))

    def test_context_processor_tema_resiliente(self):
        """O context processor deve fornecer tema padrão sem levantar exceção sob qualquer condição."""
        from .context_processors import tema
        request = self.client.get('/').wsgi_request
        ctx = tema(request)

        self.assertIn('tema', ctx)
        self.assertIn('tema_versao', ctx)
        self.assertIn('shell_template', ctx)
        self.assertIn('menu_grupos', ctx)
        self.assertEqual(ctx['shell_template'], 'layouts/shell/topo.html')


class VisibilidadePublicaTests(TestCase):
    """Testes de chaveamento de rota raiz e política anti-enumeração de rotas (Doc ① §11.1, §17.2 e §22.1 item 17)."""

    def setUp(self):
        self.client = Client()
        self.loja = Loja.objects.create(
            nome="Loja Matriz Teste",
            slug="loja-matriz-teste",
            cnpj="11.222.333/0001-44"
        )
        self.user = User.objects.create_user(
            username="operador_teste",
            password="Password123!"
        )
        self.perfil = PerfilUsuario.objects.create(
            usuario=self.user,
            loja=self.loja,
            papel=PapelUsuarioEnum.USUARIO
        )

    def test_visibilidade_ativa_serve_landing_page_para_anonimo(self):
        """Com visibilidade ativa, anônimo que acessa '/' recebe a Landing Page com status 200."""
        ConfigSite.objects.update_or_create(
            loja=None,
            defaults={'visibilidade_publica': True}
        )
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Fonte Única da Verdade")
        self.assertContains(response, reverse('login'))

    def test_visibilidade_desativada_serve_login_para_anonimo(self):
        """Com visibilidade desativada, anônimo que acessa '/' recebe a tela de login."""
        ConfigSite.objects.update_or_create(
            loja=None,
            defaults={'visibilidade_publica': False}
        )
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Acesso ao Sistema")
        self.assertContains(response, 'name="username"')
        self.assertContains(response, 'name="password"')

    def test_pagina_publica_controlavel_retorna_404_quando_desativada(self):
        """Quando a visibilidade estiver desativada, /apresentacao/ responde HTTP 404 estrito (anti-enumeração §17.2)."""
        ConfigSite.objects.update_or_create(
            loja=None,
            defaults={'visibilidade_publica': False}
        )
        response = self.client.get(reverse('site:landing'))
        self.assertEqual(response.status_code, 404)

    def test_usuario_autenticado_no_raiz_acessa_area_logada(self):
        """Usuário autenticado que acessa '/' vai diretamente para o Dashboard (área logada)."""
        self.client.login(username="operador_teste", password="Password123!")
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        # Deve exibir a navegação interna e a tela de visão geral/dashboard
        self.assertContains(response, "Visão geral")
