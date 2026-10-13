# Os códigos foram gerados com auxilio de I.A.

# Importa o módulo nativo json para decodificação de requisições AJAX com payload estruturado
import json

# Importa a classe Decimal para manipulação de porcentagens e valores monetários com precisão exata
from decimal import Decimal

# Importa atalhos do Django para renderização de páginas HTML e recuperação de instâncias com disparo de 404
from django.shortcuts import render, get_object_or_404

# Importa as classes genéricas de visualização baseadas em classe (CBVs) TemplateView e View
from django.views.generic import TemplateView, View

# Importa o mixin nativo do Django que exige que o usuário esteja devidamente autenticado na sessão
from django.contrib.auth.mixins import LoginRequiredMixin

# Importa JsonResponse para retorno estruturado em JSON para os gráficos e painéis reativos do front-end
from django.http import JsonResponse

# Importa a exceção de segurança do Django que interrompe o fluxo disparando HTTP 403 Forbidden
from django.core.exceptions import PermissionDenied

# Importa a entidade Loja representativa do tenant no particionamento de dados
from apps.tenancy.models import Loja

# Importa os mixins e funções de controle de acesso (RBAC) e verificação contratual do módulo financeiro
from apps.tenancy.permissions import (
    ModuloRequeridoMixin, FinancialAccessMixin, usuario_is_dev, pode_acessar_inteligencia_financeira
)

# Importa o modelo de Produto físico do catálogo para obtenção de preços e custos diretos
from apps.catalogo.models import Produto

# Importa as opções tarifárias de canais de venda e a entidade de parâmetros fiscais da loja
from .models import MARKETPLACE_CHOICES, ConfiguracaoTaxasLoja

# Importa a camada de serviço responsável pelo processamento matemático do motor financeiro
from .services import SimuladorPromocionalService


# Classe baseada em View que atua como interface gráfica e endpoint AJAX de inteligência financeira
class SimuladorPromocionalView(LoginRequiredMixin, ModuloRequeridoMixin, FinancialAccessMixin, View):
    # Início do bloco de docstring que detalha as funções do simulador, governança RBAC e isolamento multi-tenant
    """
    O QUE FAZ: Interface interativa e endpoint AJAX para simulação financeira e formação de preço promocional.
    POR QUE FAZ: Fornece ao lojista análise de viabilidade, margem líquida em tempo real e volume de compensação (Q_meta) antes de aplicar descontos.
    PERMISSÕES RBAC: DEV, ADMIN e SUPERVISOR (FinancialAccessMixin / RN-09). USUARIO é bloqueado com 403 Forbidden.
    MULTI-TENANCY: Filtra os produtos da loja do usuário e utiliza os parâmetros fiscais do tenant.
    """
    # Fim do bloco de documentação estrutural da visualização

    # Define o módulo contratual exigido para acesso às rotinas financeiras
    modulo_requerido = 'financeiro'

    # Especifica o arquivo de template HTML que renderiza a interface interativa do simulador
    template_name = 'financeiro/simulador_promocional.html'

    # Método GET encarregado de carregar a tela, os produtos elegíveis e os canais de marketplace disponíveis
    def get(self, request, *args, **kwargs):
        # Obtém a referência do usuário autenticado na requisição
        user = request.user

        # Verifica se o usuário autenticado possui privilégio de desenvolvedor global (DEV)
        is_dev = usuario_is_dev(user)

        # Se for desenvolvedor, permite visualizar e alternar produtos de qualquer tenant cadastrado
        if is_dev:
            # Lista todas as lojas ativas cadastradas no sistema ordenadas alfabeticamente
            lojas = Loja.objects.filter(ativo=True).order_by('nome')
            # Recupera eventual filtro de loja informado via parâmetro GET
            loja_selecionada_id = request.GET.get('loja', '')
            # Se uma loja específica foi selecionada pelo desenvolvedor, filtra os produtos ativos dela
            if loja_selecionada_id:
                produtos = Produto.objects.filter(loja_id=loja_selecionada_id, status='ATIVO').order_by('nome')
            # Caso contrário, exibe os produtos ativos de todas as lojas
            else:
                produtos = Produto.objects.filter(status='ATIVO').order_by('nome')
        # Regra para operadores e gestores comuns (ADMIN e SUPERVISOR) vinculados a um tenant específico
        else:
            # Obtém o perfil estendido do usuário logado
            perfil = getattr(user, 'perfil', None)
            # Restringe o escopo de lojas exclusivamente à própria loja do usuário
            lojas = [perfil.loja] if perfil and perfil.loja else []
            # Filtra estritamente os produtos ativos pertencentes à loja do operador
            produtos = Produto.objects.filter(loja=perfil.loja, status='ATIVO').order_by('nome') if perfil and perfil.loja else []

        # Monta o dicionário de contexto repassado para o motor de templates
        context = {
            'is_dev': is_dev,
            'lojas': lojas,
            'produtos': produtos,
            'canais': MARKETPLACE_CHOICES,
        }

        # Renderiza a página HTML entregando o contexto estruturado
        return render(request, self.template_name, context)

    # Método POST responsável por processar o cálculo da simulação sob demanda e retornar a telemetria em JSON
    def post(self, request, *args, **kwargs):
        # Captura o usuário executor da requisição
        user = request.user

        # Bloco protegido para extração e decodificação dos dados enviados (JSON ou Form POST tradicional)
        try:
            # Se a requisição contiver cabeçalho indicando carga JSON (chamada AJAX moderna)
            if request.content_type == 'application/json':
                # Decodifica o corpo da requisição em UTF-8 e carrega no dicionário Python
                data = json.loads(request.body.decode('utf-8'))
            # Se for submissão via formulário convencional
            else:
                data = request.POST
        # Em caso de falha na decodificação do corpo JSON, adota o request.POST como fallback
        except Exception:
            data = request.POST

        # Extrai o identificador primário do produto selecionado
        produto_id = data.get('produto_id')

        # Extrai o canal de marketplace selecionado, adotando 'mercadolivre_classico' como padrão
        canal_nome = data.get('canal', 'mercadolivre_classico')

        # Converte o percentual de desconto informado para o tipo Decimal de alta precisão (padrão 10.0%)
        desconto_pct = Decimal(str(data.get('desconto_pct', '10.0')))

        # Converte o volume mensal base informado em número inteiro (padrão 100 unidades)
        volume_mensal = int(data.get('volume_mensal', 100))

        # Validação defensiva: se nenhum produto foi informado no payload, rejeita com HTTP 400 Bad Request
        if not produto_id:
            return JsonResponse({'erro': 'Selecione um produto para simular.'}, status=400)

        # Recupera o produto no catálogo pela chave primária ou interrompe com HTTP 404
        produto = get_object_or_404(Produto, pk=produto_id)

        # Ownership Check multi-tenant
        # Se não for usuário DEV global, valida se o produto selecionado pertence estritamente à mesma loja do usuário
        if not usuario_is_dev(user):
            perfil = getattr(user, 'perfil', None)
            # Se o usuário não tiver loja ou se o ID da loja do produto diferir da loja do perfil
            if not perfil or not perfil.loja or produto.loja_id != perfil.loja_id:
                # Bloqueia a execução disparando HTTP 403 Forbidden para impedir espionagem de custos entre concorrentes
                raise PermissionDenied("Acesso negado: o produto selecionado pertence a outra loja.")

        # Dispara o motor de inteligência financeira através da camada de serviço
        resultado = SimuladorPromocionalService.simular_impacto_promocional(
            produto=produto,
            canal_nome=canal_nome,
            percentual_desconto=desconto_pct,
            volume_estimado_mensal=volume_mensal
        )

        # Retorna o resultado completo da simulação (margens, elasticidade, status) em formato JSON
        return JsonResponse(resultado)


# View para visualização e edição de parâmetros fiscais e taxas de canais da Loja
class ConfiguracaoTaxasLojaUpdateView(LoginRequiredMixin, ModuloRequeridoMixin, FinancialAccessMixin, View):
    """
    O QUE FAZ: Interface web responsiva para consulta e edição das alíquotas fiscais e taxas de canais por loja.
    POR QUE FAZ: Permite que administradores configurem taxas, alíquota de imposto, embalagem e margem mínima diretamente pelo sistema (US #18).
    PERMISSÕES RBAC: DEV, ADMIN e SUPERVISOR (SUPERVISOR apenas leitura; ADMIN e DEV podem salvar).
    MULTI-TENANCY: Cada operador acessa estritamente os parâmetros do seu próprio tenant.
    """
    modulo_requerido = 'financeiro'
    template_name = 'financeiro/configuracao_taxas.html'

    def get_loja(self, request):
        if usuario_is_dev(request.user):
            loja_id = request.GET.get('loja')
            if loja_id:
                return get_object_or_404(Loja, pk=loja_id, ativo=True)
            perfil = getattr(request.user, 'perfil', None)
            if perfil and perfil.loja:
                return perfil.loja
            return Loja.objects.filter(ativo=True).first()
        perfil = getattr(request.user, 'perfil', None)
        if not perfil or not perfil.loja:
            raise PermissionDenied("Acesso negado: usuário não vinculado a uma loja.")
        return perfil.loja

    def get(self, request, *args, **kwargs):
        from .forms import ConfiguracaoTaxasLojaForm
        loja = self.get_loja(request)
        config, _ = ConfiguracaoTaxasLoja.objects.get_or_create(
            loja=loja,
            defaults={
                'aliquota_imposto': Decimal('0.0400'),
                'custo_embalagem_padrao': Decimal('2.50'),
                'margem_minima_seguranca': Decimal('0.1500'),
                'custos_fixos_mensais': Decimal('0.00'),
            }
        )
        form = ConfiguracaoTaxasLojaForm(instance=config)

        # Garante canais provisionados para a loja
        from .models import ParametroCanalMarketplace
        canais_loja = []
        for c_val, c_lbl in MARKETPLACE_CHOICES:
            p_canal = SimuladorPromocionalService.obter_parametros_canal(loja, c_val)
            canais_loja.append(p_canal)

        todas_lojas = Loja.objects.filter(ativo=True).order_by('nome') if usuario_is_dev(request.user) else []

        context = {
            'form': form,
            'config': config,
            'loja': loja,
            'canais_loja': canais_loja,
            'is_dev': usuario_is_dev(request.user),
            'todas_lojas': todas_lojas,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        from django.contrib import messages
        from django.shortcuts import redirect
        from .forms import ConfiguracaoTaxasLojaForm
        from .models import ParametroCanalMarketplace

        loja = self.get_loja(request)
        perfil = getattr(request.user, 'perfil', None)
        # Se for usuário com perfil SUPERVISOR ou sem permissão de escrita, bloqueia mutações
        if not usuario_is_dev(request.user):
            if perfil and perfil.papel == 'SUPERVISOR':
                raise PermissionDenied("Acesso negado: seu perfil possui apenas permissão de leitura.")

        config, _ = ConfiguracaoTaxasLoja.objects.get_or_create(loja=loja)
        form = ConfiguracaoTaxasLojaForm(request.POST, instance=config)
        if form.is_valid():
            form.save()

            # Processa eventuais atualizações de taxas dos canais
            for c_val, _ in MARKETPLACE_CHOICES:
                comissao_key = f"canal_{c_val}_comissao"
                frete_piso_key = f"canal_{c_val}_frete_piso"
                frete_acima_key = f"canal_{c_val}_frete_acima"
                taxa_fixa_key = f"canal_{c_val}_taxa_fixa"

                if comissao_key in request.POST:
                    param = SimuladorPromocionalService.obter_parametros_canal(loja, c_val)
                    try:
                        param.comissao_padrao = Decimal(str(request.POST[comissao_key]))
                        param.frete_gratis_piso = Decimal(str(request.POST[frete_piso_key]))
                        param.taxa_frete_acima_limite = Decimal(str(request.POST[frete_acima_key]))
                        param.taxa_fixa_abaixo_limite = Decimal(str(request.POST[taxa_fixa_key]))
                        param.save()
                    except (ValueError, TypeError):
                        pass

            messages.success(request, f"Parâmetros financeiros da loja '{loja.nome}' atualizados com sucesso!")
            return redirect('configuracao_taxas')
        else:
            messages.error(request, "Por favor, corrija os erros no formulário.")
            canais_loja = [SimuladorPromocionalService.obter_parametros_canal(loja, c[0]) for c in MARKETPLACE_CHOICES]
            todas_lojas = Loja.objects.filter(ativo=True).order_by('nome') if usuario_is_dev(request.user) else []
            return render(request, self.template_name, {
                'form': form,
                'config': config,
                'loja': loja,
                'canais_loja': canais_loja,
                'is_dev': usuario_is_dev(request.user),
                'todas_lojas': todas_lojas,
            })


# Rota/View para cálculo de margem e precificação via endpoint (RTM / US #17)
class CalcularMargemView(LoginRequiredMixin, ModuloRequeridoMixin, FinancialAccessMixin, View):
    """
    O QUE FAZ: Endpoint AJAX/REST para cálculo de margem, frete e markup de um produto.
    POR QUE FAZ: Atende à rota identificada na RTM (/financeiro/margem/calcular/).
    """
    modulo_requerido = 'financeiro'

    def post(self, request, *args, **kwargs):
        try:
            if request.content_type == 'application/json':
                data = json.loads(request.body.decode('utf-8'))
            else:
                data = request.POST
        except Exception:
            data = request.POST

        produto_id = data.get('produto_id')
        if not produto_id:
            return JsonResponse({'erro': 'Informe o produto_id'}, status=400)

        produto = get_object_or_404(Produto, pk=produto_id)
        if not usuario_is_dev(request.user):
            perfil = getattr(request.user, 'perfil', None)
            if not perfil or not perfil.loja or produto.loja_id != perfil.loja_id:
                raise PermissionDenied("Acesso negado: produto pertence a outra loja.")

        canal_nome = data.get('canal', 'mercadolivre_classico')
        desconto = Decimal(str(data.get('desconto_pct', '0.0')))
        resultado = SimuladorPromocionalService.simular_impacto_promocional(
            produto=produto,
            canal_nome=canal_nome,
            percentual_desconto=desconto,
            volume_estimado_mensal=int(data.get('volume_mensal', 100))
        )
        return JsonResponse(resultado)
