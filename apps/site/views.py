# Os códigos foram gerados com auxilio de I.A.
"""
O QUE FAZ: Views do módulo de Site, Landing Page, Visibilidade Pública e Endpoint /tema.css (Doc ① §11.1 e §11.12).
POR QUE FAZ:
  - Serve o CSS dinâmico /tema.css com cache longo, versionado e sanitizado contra CSS injection.
  - Implementa o chaveamento dinâmico da rota raiz '/' baseado em 'site.visibilidade_publica'.
  - Garante resposta HTTP 404 estrita para páginas públicas quando a visibilidade estiver desativada (política anti-enumeração §17.2).
PERMISSÕES RBAC: Rota '/' e '/tema.css' são públicas.
MULTI-TENANCY: Resolução via get_tenant(request).
"""

from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.http import require_GET
from django.conf import settings

from .models import ConfigTema, ConfigSite
from .utils_tema import gerar_css_tema
from apps.core.tenancy import get_tenant


@require_GET
def tema_css_view(request):
    """
    O QUE FAZ: Endpoint público que serve o CSS gerado do tema ativo (Doc ① §11.12 item 6).
    POR QUE FAZ: Permite que tanto páginas públicas (login, landing) quanto internas consumam os tokens visuais.
    SEGURANÇA: Blindagem estrita contra CSS injection (apenas hexadecimais validados).
    CACHE: Cache-Control longo e imutável; a versão muda na URL (?v=<hash>).
    """
    tenant = get_tenant(request)
    config_tema = ConfigTema.get_tema_ativo(loja=tenant)

    css_content = gerar_css_tema(
        cor_fundos=config_tema.cor_fundos,
        cor_destaques=config_tema.cor_destaques,
        cor_escritas=config_tema.cor_escritas
    )

    response = HttpResponse(css_content, content_type='text/css; charset=utf-8')
    # Cache longo imutável (1 ano)
    response['Cache-Control'] = 'public, max-age=31536000, immutable'
    return response


class RaizView(View):
    """
    O QUE FAZ: Controla a navegação da rota raiz '/' comutando dinamicamente entre Landing Page e Login (Doc ① §11.1).
    POR QUE FAZ:
      - Usuário já autenticado: renderiza diretamente o Dashboard da aplicação.
      - Usuário anônimo + Visibilidade Ativa: renderiza Landing Page com botão 'Login' destacado.
      - Usuário anônimo + Visibilidade Desativada: serve a tela de Login diretamente.
    """
    def dispatch(self, request, *args, **kwargs):
        # 1. Se o usuário já está autenticado, despacha o DashboardHomeView
        if request.user.is_authenticated:
            try:
                from apps.tenancy.views import DashboardHomeView
                return DashboardHomeView.as_view()(request, *args, **kwargs)
            except Exception:
                return redirect('catalogo:produto_list')

        # 2. Usuário anônimo: avalia a flag de visibilidade pública
        tenant = get_tenant(request)
        visibilidade_ativa = ConfigSite.is_visibilidade_publica_ativa(loja=tenant)

        if visibilidade_ativa:
            # Serve a Landing Page institucional
            return render(request, 'site/landing.html', {
                'visibilidade_ativa': True
            })

        # Visibilidade desativada: serve a tela de login
        from django.contrib.auth.views import LoginView
        return LoginView.as_view(template_name='registration/login.html')(request, *args, **kwargs)


class LandingPageView(View):
    """
    O QUE FAZ: Página de apresentação detalhada e institucional do produto.
    POR QUE FAZ: Demonstra recursos do Hub.
    POLÍTICA ANTI-ENUMERAÇÃO (§17.2): Quando a visibilidade pública estiver desativada,
    usuários anônimos recebem obrigatoriamente HTTP 404 (idêntico a rota inexistente).
    """
    def get(self, request, *args, **kwargs):
        tenant = get_tenant(request)
        visibilidade_ativa = ConfigSite.is_visibilidade_publica_ativa(loja=tenant)

        # Se desativada e usuário não autenticado, bloqueia com 404 estrito (Doc ① §11.1 e §17.2)
        if not visibilidade_ativa and not request.user.is_authenticated:
            raise Http404("Página não encontrada.")

        return render(request, 'site/landing.html', {
            'visibilidade_ativa': visibilidade_ativa
        })
