import zlib

from .fec import NSYM, add_fec, remove_fec

MAX_PAYLOAD = 200  # reduzido para caber overhead RS


def pack(payload: bytes, seq: int = 0) -> bytes:
    """Cria pacote com Reed-Solomon + header + CRC"""
    if len(payload) > MAX_PAYLOAD:
        raise ValueError(f"Payload máximo {MAX_PAYLOAD} bytes")

    fec_payload = add_fec(payload)
    encoded_len = len(fec_payload)

    header = b"QC" + (seq % 65536).to_bytes(2, "big") + len(payload).to_bytes(2, "big")
    padded = fec_payload + b"\x00" * (248 - encoded_len)
    data = header + padded
    crc = zlib.crc32(data).to_bytes(4, "big")
    return data + crc


def unpack(raw: bytes):
    """Verifica CRC e aplica Reed-Solomon (retorna payload original corrigido)"""
    if len(raw) != 258:
        return None
    header = raw[:6]
    if header[:2] != b"QC":
        return None
    original_len = int.from_bytes(header[4:6], "big")
    if original_len > MAX_PAYLOAD:
        return None

    # CRC
    if zlib.crc32(raw[:-4]).to_bytes(4, "big") != raw[-4:]:
        return None

    seq = int.from_bytes(header[2:4], "big")

    # Recupera exatamente o bloco codificado (sem padding)
    encoded_len = original_len + NSYM
    fec_data = raw[6 : 6 + encoded_len]

    try:
        payload = remove_fec(fec_data)
        return seq, payload[:original_len]
    except Exception:
        return None
