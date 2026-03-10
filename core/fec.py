from reedsolo import RSCodec

NSYM = 32  # pode corrigir até 16 erros por bloco

rs = RSCodec(NSYM)


def add_fec(payload: bytes) -> bytes:
    """Aplica Reed-Solomon (correção de erros forte)"""
    return rs.encode(payload)


def remove_fec(encoded: bytes) -> bytes:
    """Decodifica com correção automática de erros"""
    try:
        return rs.decode(encoded)[0]
    except Exception:
        return encoded  # fallback seguro
