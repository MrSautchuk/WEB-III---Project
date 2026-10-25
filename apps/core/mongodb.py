# Os códigos foram gerados com auxilio de I.A.
"""
Módulo utilitário de integração com MongoDB Atlas (NoSQL) — Hub Central de Marketplaces.
Atende ao critério de banco de dados NoSQL da disciplina de Web III (Sprint 2 / US-30).

Garante degradação graciosa (graceful degradation):
- Se a variável MONGODB_URI estiver presente e a conexão for bem-sucedida, registra eventos analíticos no MongoDB.
- Se MONGODB_URI estiver vazia ou o cluster estiver inacessível/offline, registra em log local sem travar nenhuma operação do Django.
"""

import logging
from typing import Optional, Any, Dict
from django.conf import settings

logger = logging.getLogger(__name__)

_mongo_client = None


def get_mongodb_client():
    """
    Retorna o cliente singleton do PyMongo configurado a partir de MONGODB_URI.
    Retorna None se a URI não estiver configurada ou se a conexão falhar.
    """
    global _mongo_client
    if _mongo_client is not None:
        return _mongo_client

    mongo_uri = getattr(settings, 'MONGODB_URI', '') or ''
    if not mongo_uri.strip():
        logger.debug("[MongoDB] MONGODB_URI não configurada. Operando em modo desacoplado.")
        return None

    try:
        import pymongo
        _mongo_client = pymongo.MongoClient(
            mongo_uri,
            serverSelectionTimeoutMS=2000,
            connectTimeoutMS=2000,
        )
        return _mongo_client
    except Exception as exc:
        logger.warning(f"[MongoDB] Falha ao inicializar MongoClient: {exc}")
        return None


def get_mongodb_database():
    """
    Retorna a instância do Database no MongoDB Atlas ou None caso indisponível.
    """
    client = get_mongodb_client()
    if client is None:
        return None

    db_name = getattr(settings, 'MONGODB_DB_NAME', 'hub_marketplace_db')
    try:
        return client[db_name]
    except Exception as exc:
        logger.warning(f"[MongoDB] Falha ao obter database '{db_name}': {exc}")
        return None


def log_audit_event(event_type: str, payload: Dict[str, Any], tenant_id: Optional[int] = None) -> bool:
    """
    Registra um evento analítico de auditoria ou telemetria no cluster NoSQL MongoDB Atlas.
    Se o MongoDB estiver indisponível, faz fallback para log do Django sem lançar exceções.
    
    Retorna True se persistido no MongoDB, False se executado via fallback gracioso.
    """
    import datetime

    record = {
        'event_type': event_type,
        'tenant_id': tenant_id,
        'payload': payload,
        'timestamp': datetime.datetime.now(datetime.timezone.utc),
    }

    db = get_mongodb_database()
    if db is not None:
        try:
            db['audit_events'].insert_one(record)
            return True
        except Exception as exc:
            logger.warning(f"[MongoDB] Erro ao inserir log de auditoria no MongoDB: {exc}")

    # Fallback transparente para o log da aplicação
    logger.info(f"[AUDIT LOG FALLBACK] Event={event_type} Tenant={tenant_id} Payload={payload}")
    return False
