"""Codifica um arquivo em lista de pacotes prontos para modulação."""

import zlib

from core.fec import encode as fec_encode
from core.packet import create_packet

CHUNK = 246  # 246 dados + 10 paridade = 256 payload


def encode_file(path: str) -> list[bytes]:
    with open(path, "rb") as f:
        data = zlib.compress(f.read(), level=6)

    chunks = [data[i : i + CHUNK] for i in range(0, len(data), CHUNK)]
    total = len(chunks)
    packets = []

    for idx, chunk in enumerate(chunks):
        protected = fec_encode(chunk)
        pkt = create_packet(protected, packet_id=idx, total_packets=total)
        packets.append(pkt)

    return packets


def packet_to_bits(packet: bytes) -> list[int]:
    bits = []
    for byte in packet:
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)
    return bits
