# Os códigos foram gerados com auxilio de I.A.
"""
MÓDULO DE SERVIÇOS DO DOMÍNIO DE CATÁLOGO (apps.catalogo.services)
Encapsula a lógica de negócio transacional e operações de estoque, desacoplando
as Views HTTP de detalhes de concorrência pessimista (select_for_update), auditoria
e garantindo isolamento multi-tenant obrigatório contra IDOR.
"""

from typing import Tuple
from django.db import transaction
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from apps.marketplaces.models import LogAuditoria
from apps.marketplaces.enums import EventoAuditoriaEnum
from .models import Produto, HistoricoPreco


def executar_baixa_avaria_estoque(
    produto_id: int,
    loja,
    quantidade: int,
    tipo_baixa: str,
    justificativa: str,
    usuario,
    ip_origem: str = None
) -> Tuple[Produto, int, int]:
    """
    O QUE FAZ: Executa a baixa física de saldo por motivo de avaria/perda com bloqueio
               pessimista (select_for_update), histórico e auditoria.
    POR QUE FAZ: Desacopla regras de concorrência e auditoria da camada de apresentação
                 (View), eliminando Fat View e blindando contra IDOR (CWE-639).
    MULTI-TENANCY: O filtro 'loja' é estritamente obrigatório no lock transacional.
    RETORNA: Tupla (produto, saldo_anterior, novo_saldo).
    """
    if not loja:
        raise PermissionDenied("Operação não permitida: loja inquilina (tenant) não identificada.")

    with transaction.atomic():
        # Busca o produto com bloqueio de concorrência garantindo isolamento de loja
        prod_locked = Produto.objects.select_for_update().get(pk=produto_id, loja=loja)
        saldo_anterior = prod_locked.estoque
        novo_saldo = saldo_anterior - quantidade
        prod_locked.estoque = novo_saldo
        prod_locked._usuario_operacao = usuario
        prod_locked.save(update_fields=['estoque', 'atualizado_em'])

        # Registra no histórico de preço/estoque
        HistoricoPreco.objects.create(
            produto=prod_locked,
            loja=prod_locked.loja,
            preco_anterior=prod_locked.preco,
            preco_novo=prod_locked.preco,
            estoque_anterior=saldo_anterior,
            estoque_novo=novo_saldo,
            usuario=usuario,
            motivo=f"Baixa por Avaria ({tipo_baixa}): {justificativa}"
        )

        # Registra auditoria
        LogAuditoria.objects.create(
            loja=prod_locked.loja,
            autor=usuario,
            evento=EventoAuditoriaEnum.BAIXA_AVARIA,
            detalhes=(
                f"Baixa de {quantidade} un. do produto '{prod_locked.sku}' por motivo '{tipo_baixa}'. "
                f"Saldo anterior: {saldo_anterior} -> Novo saldo: {novo_saldo}. "
                f"Justificativa: {justificativa}"
            ),
            ip_origem=ip_origem
        )

    return prod_locked, saldo_anterior, novo_saldo


def executar_ajuste_geral_estoque(
    produto_id: int,
    loja,
    novo_saldo: int,
    tipo_ajuste: str,
    justificativa: str,
    usuario,
    ip_origem: str = None
) -> Tuple[Produto, int, int]:
    """
    O QUE FAZ: Executa o ajuste geral de balanço de inventário com bloqueio pessimista,
               histórico e log de auditoria isolados por loja.
    MULTI-TENANCY: Filtra estritamente por produto_id e loja para evitar acesso cross-tenant.
    RETORNA: Tupla (produto, saldo_anterior, novo_saldo).
    """
    if not loja:
        raise PermissionDenied("Operação não permitida: loja inquilina (tenant) não identificada.")

    with transaction.atomic():
        prod_locked = Produto.objects.select_for_update().get(pk=produto_id, loja=loja)
        saldo_anterior = prod_locked.estoque
        prod_locked.estoque = novo_saldo
        prod_locked._usuario_operacao = usuario
        prod_locked.save(update_fields=['estoque', 'atualizado_em'])

        HistoricoPreco.objects.create(
            produto=prod_locked,
            loja=prod_locked.loja,
            preco_anterior=prod_locked.preco,
            preco_novo=prod_locked.preco,
            estoque_anterior=saldo_anterior,
            estoque_novo=novo_saldo,
            usuario=usuario,
            motivo=f"Ajuste Geral ({tipo_ajuste}): {justificativa}"
        )

        LogAuditoria.objects.create(
            loja=prod_locked.loja,
            autor=usuario,
            evento=EventoAuditoriaEnum.AJUSTE_ESTOQUE,
            detalhes=(
                f"Ajuste geral de estoque do SKU '{prod_locked.sku}' ({tipo_ajuste}). "
                f"Saldo anterior: {saldo_anterior} -> Novo saldo: {novo_saldo}. "
                f"Justificativa: {justificativa}"
            ),
            ip_origem=ip_origem
        )

    return prod_locked, saldo_anterior, novo_saldo
