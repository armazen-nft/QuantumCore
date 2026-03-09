"""Serialização e desserialização de pacotes OpenFM."""

import os
import struct
import zlib

VERSION = 0x01
NODE_ID = int.from_bytes(os.urandom(4), "big")  # gerado na inicialização
HEADER_FMT = ">BIHHHI"  # version(1) node_id(4) pkt_id(2) total(2) size(2) crc(4)
HEADER_SIZE = struct.calcsize(HEADER_FMT)  # 15 bytes


def create_packet(payload: bytes, packet_id: int, total_packets: int = 0) -> bytes:
    crc = zlib.crc32(payload) & 0xFFFFFFFF
    header = struct.pack(
        HEADER_FMT,
        VERSION,
        NODE_ID,
        packet_id,
        total_packets,
        len(payload),
        crc,
    )
    return header + payload


def parse_packet(data: bytes) -> dict | None:
    if len(data) < HEADER_SIZE:
        return None

    version, node_id, pkt_id, total, size, crc = struct.unpack(
        HEADER_FMT,
        data[:HEADER_SIZE],
    )
    payload = data[HEADER_SIZE : HEADER_SIZE + size]
    if zlib.crc32(payload) & 0xFFFFFFFF != crc:
        return None

    return {
        "version": version,
        "node_id": node_id,
        "packet_id": pkt_id,
        "total_packets": total,
        "payload": payload,
    }
