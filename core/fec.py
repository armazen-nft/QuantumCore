def add_fec(payload: bytes) -> bytes:
    """FEC simples por repetição 3x."""
    return payload * 3


def remove_fec(data: bytes) -> bytes:
    """Recupera payload assumindo repetição 3x."""
    if len(data) % 3 != 0:
        return data
    chunk = len(data) // 3
    return data[:chunk]
