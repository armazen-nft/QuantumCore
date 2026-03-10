import struct
import zlib
from typing import Optional, Tuple


def pack(payload: bytes, seq: int = 0) -> bytes:
    """Empacota payload com sequência + CRC32."""
    crc = zlib.crc32(payload) & 0xFFFFFFFF
    header = struct.pack(">IIH", seq & 0xFFFFFFFF, crc, len(payload) & 0xFFFF)
    return header + payload


def unpack(packet: bytes) -> Optional[Tuple[int, bytes]]:
    """Desempacota e valida CRC. Retorna (seq, payload) ou None."""
    if len(packet) < 10:
        return None

    seq, crc, size = struct.unpack(">IIH", packet[:10])
    payload = packet[10:10 + size]
    if len(payload) != size:
        return None

    if (zlib.crc32(payload) & 0xFFFFFFFF) != crc:
        return None

    return seq, payload
