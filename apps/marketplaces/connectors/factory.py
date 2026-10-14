# Os códigos foram gerados com auxilio de I.A.

# Importa o tipo Optional da biblioteca typing para permitir argumentos que podem ser nulos
from typing import Optional

# Importa o modelo ContaMarketplace que encapsula as credenciais e configurações de integração da loja
from apps.marketplaces.models import ContaMarketplace

# Importa o enum CanalMarketplaceEnum contendo as constantes representativas de cada marketplace suportado
from apps.marketplaces.enums import CanalMarketplaceEnum

# Importa a classe abstrata base BaseMarketplaceConnector para anotação de tipagem do retorno
from .base import BaseMarketplaceConnector

# Importa a implementação concreta do conector do Mercado Livre
from .mercadolivre import MercadoLivreConnector

# Importa a implementação concreta do conector da plataforma Shopee
from .shopee import ShopeeConnector

# Importa a implementação concreta do conector da plataforma Magazine Luiza
from .magalu import MagaluConnector

# Importa a implementação concreta do conector da Amazon SP-API
from .amazon import AmazonConnector


# Dicionário de registro (Registry Pattern) mapeando os enums de canais às suas respectivas classes concretas
CONNECTOR_REGISTRY = {
    # Mapeia a constante MERCADOLIVRE para a classe MercadoLivreConnector
    CanalMarketplaceEnum.MERCADOLIVRE: MercadoLivreConnector,
    # Mapeia a constante SHOPEE para a classe ShopeeConnector
    CanalMarketplaceEnum.SHOPEE: ShopeeConnector,
    # Mapeia a constante MAGALU para a classe MagaluConnector
    CanalMarketplaceEnum.MAGALU: MagaluConnector,
    # Mapeia a constante AMAZON para a classe AmazonConnector
    CanalMarketplaceEnum.AMAZON: AmazonConnector,
}


# Função fábrica (Factory Pattern) que resolve e instancia o conector adequado com base na instância de ContaMarketplace
def get_connector_for_conta(conta: ContaMarketplace) -> BaseMarketplaceConnector:
    # Início do bloco de docstring que documenta o padrão de projeto, responsabilidades e contexto multi-tenant
    """
    O QUE FAZ: Instancia e retorna o conector adequado para a ContaMarketplace informada (Factory Pattern).
    POR QUE FAZ: Centraliza a resolução do conector correto sem espalhar condicionais de canal no código.
    PERMISSÕES RBAC: Infraestrutura / Serviços.
    MULTI-TENANCY: O conector retornado fica vinculado aos dados e credenciais da conta do tenant.
    """
    # Fim do bloco de documentação estrutural da função

    # Busca a classe do conector registrada para o canal da conta
    if not conta or not getattr(conta, 'canal', None):
        raise ValueError("ContaMarketplace inválida ou canal não especificado.")

    connector_cls = CONNECTOR_REGISTRY.get(conta.canal)
    if not connector_cls:
        raise ValueError(
            f"Canal de marketplace '{conta.canal}' não é suportado pelo Hub ou conector não registrado."
        )

    # Instancia a classe do conector passando a conta de integração vinculada e retorna o objeto configurado
    return connector_cls(conta=conta)


# Função fábrica alternativa que instancia o conector a partir da string/chave do canal e conta opcional
def get_connector_for_canal(canal: str, conta: Optional[ContaMarketplace] = None) -> BaseMarketplaceConnector:
    # Início do bloco de docstring informativa da função
    """
    O QUE FAZ: Instancia e retorna o conector com base na chave do canal.
    """

    if not canal:
        raise ValueError("Identificador do canal de marketplace não pode ser nulo ou vazio.")

    # Busca a classe do conector pela chave textual do canal
    connector_cls = CONNECTOR_REGISTRY.get(canal)
    if not connector_cls:
        raise ValueError(
            f"Canal de marketplace '{canal}' não é suportado pelo Hub ou conector não registrado."
        )

    # Instancia e retorna o conector correspondente associando a conta informada (caso fornecida)
    return connector_cls(conta=conta)