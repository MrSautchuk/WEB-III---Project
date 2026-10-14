# Os códigos foram gerados com auxilio de I.A.

# Início do bloco de docstring que documenta o objetivo do utilitário de validação criptográfica de Webhooks
"""
O QUE FAZ: Módulo utilitário para validação simétrica de assinaturas criptográficas HMAC para webhooks HTTP.
POR QUE FAZ: Neutraliza requisições forjadas ou sem assinatura válida com checagem criptográfica segura HMAC (compare_digest).
"""
# Fim do bloco de documentação estrutural

# Importa o módulo nativo hmac para geração e comparação em tempo constante de Message Authentication Codes
import hmac

# Importa o módulo nativo hashlib para disponibilizar a função de hash criptográfico SHA-256
import hashlib

# Importa o módulo nativo time para eventuais medições temporais e manipulação de timestamps
import time

# Importa o tipo Tuple para tipagem estática do retorno da função
from typing import Tuple


# Declaração da função responsável por validar assinaturas HMAC de webhooks e extrair timestamps de requisições
def validar_assinatura_e_anti_replay(request, secret: str, canal: str = 'mercadolivre', max_age_seconds: int = 300) -> Tuple[bool, int, str]:
    # Início do bloco de docstring que documenta os parâmetros, comportamento de tolerância e a tupla de retorno
    """
    Valida a autenticidade da assinatura criptográfica HMAC.
    Extrai o timestamp caso ele componha o hash do canal, sem bloquear requisições por janela temporal expirada.
    Retorna (valido: bool, status_code: int, mensagem: str).
    """
    # Fim da docstring explicativa da função

    # Comportamento Fail-Closed (US #12 / CWE-347): Rejeita sumariamente se secret não configurado
    if not secret:
        return False, 401, "Webhook secret não configurado para este canal."

    # 1. Extração do timestamp dos cabeçalhos
    raw_ts = (
        request.META.get('HTTP_X_TIMESTAMP')
        or request.META.get('HTTP_TIMESTAMP')
        or request.META.get('HTTP_X_REQUEST_TIMESTAMP')
    )

    sig_header = (
        request.META.get('HTTP_X_SIGNATURE')
        or request.META.get('HTTP_AUTHORIZATION')
        or request.META.get('HTTP_X_HUB_SIGNATURE_256')
        or request.META.get('HTTP_SIGNATURE')
        or ''
    )

    # Se o cabeçalho x-signature contiver ts=123...,v1=abc... (padrão oficial Mercado Livre)
    if 'ts=' in sig_header:
        parts = sig_header.split(',')
        for part in parts:
            part = part.strip()
            if part.startswith('ts='):
                raw_ts = part.split('=', 1)[1]
            elif part.startswith('v1='):
                sig_header = part.split('=', 1)[1]

    # Validação da Janela Anti-Replay Temporal (US #15 / CWE-294)
    if raw_ts:
        try:
            ts_int = int(raw_ts)
            # Se for milissegundos (13 dígitos), converte para segundos
            if ts_int > 1e11:
                ts_int = ts_int // 1000
            agora = int(time.time())
            if abs(agora - ts_int) > max_age_seconds:
                return False, 401, f"Timestamp do webhook expirado (tolerância de {max_age_seconds}s excedida)."
        except (ValueError, TypeError):
            return False, 401, "Timestamp inválido no cabeçalho do webhook."

    # 2. Validação da Assinatura HMAC
    if not sig_header:
        return False, 401, "Cabeçalho de assinatura HMAC ausente."

    # Remove eventuais espaços em branco nas extremidades da assinatura fornecida
    provided_sig = sig_header.strip()

    # Normaliza a assinatura removendo prefixo 'sha256=' caso presente (padrão GitHub/Meta)
    if provided_sig.startswith('sha256='):
        provided_sig = provided_sig.split('=', 1)[1]
    # Normaliza a assinatura removendo prefixo 'v1=' caso ainda remanescente
    elif provided_sig.startswith('v1='):
        provided_sig = provided_sig.split('=', 1)[1]
    # Normaliza a assinatura removendo prefixo 'Bearer ' caso o token tenha sido enviado via Authorization header
    elif provided_sig.lower().startswith('bearer '):
        provided_sig = provided_sig[7:].strip()

    # Converte a chave secreta em sequência de bytes UTF-8 para o algoritmo HMAC
    secret_bytes = secret.encode('utf-8')

    # Recupera o corpo bruto (bytes) da requisição para cálculo do resumo criptográfico
    body_bytes = request.body if hasattr(request, 'body') else b''

    # Possíveis padrões canônicos aceitos pelos marketplaces
    # Lista para armazenar as variações de payload aceitas na montagem do hash
    candidate_hashes = []

    # A. HMAC sobre o corpo puro (padrão HMAC-SHA256)
    # Calcula e anexa o HMAC-SHA256 gerado diretamente sobre os bytes do corpo da requisição
    candidate_hashes.append(hmac.new(secret_bytes, body_bytes, hashlib.sha256).hexdigest())

    # B. HMAC sobre ts + corpo (padrão Shopee / Meli com ts)
    # Se um timestamp foi fornecido na requisição, gera as variações canônicas de concatenação
    if raw_ts:
        ts_str = str(raw_ts)
        # Variação 1: Concatena timestamp e corpo separados por ponto (ts.body)
        candidate_hashes.append(hmac.new(secret_bytes, f"{ts_str}.{body_bytes.decode('utf-8', errors='ignore')}".encode('utf-8'), hashlib.sha256).hexdigest())
        # Variação 2: Concatena bytes do timestamp diretamente antes dos bytes do corpo (ts + body)
        candidate_hashes.append(hmac.new(secret_bytes, ts_str.encode('utf-8') + body_bytes, hashlib.sha256).hexdigest())
        # Variação 3: Concatena com prefixo estruturado (ts:{timestamp}; + body)
        candidate_hashes.append(hmac.new(secret_bytes, f"ts:{ts_str};".encode('utf-8') + body_bytes, hashlib.sha256).hexdigest())

    # Comparação segura contra timing attacks
    # Itera sobre os hashes candidatos comparando com a assinatura fornecida em tempo constante (evitando side-channel attacks)
    for expected in candidate_hashes:
        if hmac.compare_digest(provided_sig.lower(), expected.lower()):
            # Retorna tupla de sucesso com HTTP 200 caso alguma combinação seja criptograficamente idêntica
            return True, 200, "Assinatura válida."

    # Se nenhuma das variações conferir com a assinatura enviada pelo canal externo, rejeita com HTTP 401
    return False, 401, "Assinatura HMAC inválida."
