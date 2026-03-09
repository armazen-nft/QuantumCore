"""Reconstrói um arquivo a partir de pacotes recebidos."""

import zlib

from core.fec import decode as fec_decode
from core.packet import parse_packet


def bits_to_bytes(bits: list[int]) -> bytes:
    out = bytearray()
    for i in range(0, len(bits) - 7, 8):
        byte = 0
        for j in range(8):
            byte = (byte << 1) | bits[i + j]
        out.append(byte)
    return bytes(out)


def decode_packets(raw_packets: list[bytes]) -> bytes | None:
    parsed = {}
    for raw in raw_packets:
        p = parse_packet(raw)
        if p:
            try:
                payload = fec_decode(p["payload"])
                parsed[p["packet_id"]] = (payload, p["total_packets"])
            except Exception:
                pass

    if not parsed:
        return None

    total = list(parsed.values())[0][1]
    if len(parsed) < total:
        return None  # pacotes faltando

    ordered = b"".join(parsed[i][0] for i in sorted(parsed))
    return zlib.decompress(ordered)
