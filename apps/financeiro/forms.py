# Os códigos foram gerados com auxilio de I.A.

from django import forms
from decimal import Decimal
from .models import ConfiguracaoTaxasLoja, ParametroCanalMarketplace, MARKETPLACE_CHOICES


class ConfiguracaoTaxasLojaForm(forms.ModelForm):
    """
    Formulário para parametrização fiscal e de custos da Loja (Tenant).
    Permite configurar alíquota de imposto, custo padrão de embalagem, margem mínima e custos fixos.
    """
    class Meta:
        model = ConfiguracaoTaxasLoja
        fields = [
            'aliquota_imposto',
            'custo_embalagem_padrao',
            'margem_minima_seguranca',
            'custos_fixos_mensais',
        ]
        widgets = {
            'aliquota_imposto': forms.NumberInput(attrs={
                'class': 'form-control font-monospace',
                'step': '0.0001',
                'min': '0',
                'max': '1',
                'placeholder': '0.0400 (4%)'
            }),
            'custo_embalagem_padrao': forms.NumberInput(attrs={
                'class': 'form-control font-monospace',
                'step': '0.01',
                'min': '0',
                'placeholder': '2.50'
            }),
            'margem_minima_seguranca': forms.NumberInput(attrs={
                'class': 'form-control font-monospace',
                'step': '0.0001',
                'min': '0',
                'max': '1',
                'placeholder': '0.1500 (15%)'
            }),
            'custos_fixos_mensais': forms.NumberInput(attrs={
                'class': 'form-control font-monospace',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00'
            }),
        }
        labels = {
            'aliquota_imposto': 'Alíquota de Imposto (ex: 0.04 = 4%)',
            'custo_embalagem_padrao': 'Custo de Embalagem Padrão (R$)',
            'margem_minima_seguranca': 'Margem Líquida Mínima de Segurança (ex: 0.15 = 15%)',
            'custos_fixos_mensais': 'Custos Fixos Mensais (R$)',
        }
        help_texts = {
            'aliquota_imposto': 'Percentual incidente sobre faturamento bruto (ex: Simples Nacional 4% = 0.04).',
            'custo_embalagem_padrao': 'Custo padrão debitado de produtos sem embalagem específica.',
            'margem_minima_seguranca': 'Piso mínimo de rentabilidade desejada (ex: 15% = 0.15).',
            'custos_fixos_mensais': 'Soma mensal de aluguel, salários, softwares e despesas operacionais fixas.',
        }


class ParametroCanalMarketplaceForm(forms.ModelForm):
    """
    Formulário para configuração das regras tarifárias e de frete por canal de marketplace.
    """
    class Meta:
        model = ParametroCanalMarketplace
        fields = [
            'marketplace',
            'comissao_padrao',
            'frete_gratis_piso',
            'taxa_frete_acima_limite',
            'taxa_fixa_abaixo_limite',
        ]
        widgets = {
            'marketplace': forms.Select(attrs={'class': 'form-select'}),
            'comissao_padrao': forms.NumberInput(attrs={
                'class': 'form-control font-monospace',
                'step': '0.0001',
                'min': '0',
                'max': '1'
            }),
            'frete_gratis_piso': forms.NumberInput(attrs={
                'class': 'form-control font-monospace',
                'step': '0.01',
                'min': '0'
            }),
            'taxa_frete_acima_limite': forms.NumberInput(attrs={
                'class': 'form-control font-monospace',
                'step': '0.01',
                'min': '0'
            }),
            'taxa_fixa_abaixo_limite': forms.NumberInput(attrs={
                'class': 'form-control font-monospace',
                'step': '0.01',
                'min': '0'
            }),
        }
