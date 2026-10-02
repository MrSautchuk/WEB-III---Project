# Os códigos foram gerados com auxilio de I.A.
"""
O QUE FAZ: Views do módulo de Site, Apresentação e Endpoint /tema.css.
POR QUE FAZ:
  - Serve o CSS dinâmico /tema.css sanitizado contra CSS injection.
  - Na rota raiz '/', entrega a experiência operacional direta: Dashboard para logados e chaveamento Landing/Login para anônimos.
  - Oferece a página de apresentação em /apresentacao/ respeitando a política anti-enumeração (§17.2).
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
    Endpoint público que serve o CSS gerado do tema ativo.
    Garante sanitização estrita de hexadecimais contra CSS injection.
    """
    tenant = get_tenant(request)
    config_tema = ConfigTema.get_tema_ativo(loja=tenant)

    css_content = gerar_css_tema(
        cor_fundos=config_tema.cor_fundos,
        cor_destaques=config_tema.cor_destaques,
        cor_escritas=config_tema.cor_escritas
    )

    response = HttpResponse(css_content, content_type='text/css; charset=utf-8')
    response['Cache-Control'] = 'public, max-age=31536000, immutable'
    return response


class RaizView(View):
    """
    Controla o fluxo direto de acesso:
      - Usuário logado: acessa imediatamente o Dashboard principal (tenancy/home.html).
      - Usuário anônimo:
          * Se visibilidade pública ativa: Landing Page com status 200.
          * Se visibilidade pública desativada: Tela de login direto.
    """
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                from apps.tenancy.views import DashboardHomeView
                return DashboardHomeView.as_view()(request, *args, **kwargs)
            except Exception:
                return redirect('produto_list')

        if ConfigSite.is_visibilidade_publica_ativa():
            return render(request, 'site/landing.html', {'visibilidade_ativa': True})

        from django.contrib.auth.views import LoginView
        return LoginView.as_view(template_name='registration/login.html')(request, *args, **kwargs)


class LandingPageView(View):
    """
    Página institucional e informativa dos recursos do Hub Central de Marketplaces.
    Acessível em /apresentacao/. Responde 404 estrito se desativada (Doc ① §17.2).
    """
    def get(self, request, *args, **kwargs):
        if not ConfigSite.is_visibilidade_publica_ativa():
            raise Http404("Página desativada.")
        return render(request, 'site/landing.html', {
            'visibilidade_ativa': True
        })
