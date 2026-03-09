"""Packet serialization utilities for QuantumCore."""

from __future__ import annotations

import zlib

PACKET_SIZE = 258
HEADER_SIZE = 6
PAYLOAD_SIZE = 248
CRC_SIZE = 4
MAGIC = b"QC"


def pack(payload: bytes, seq: int = 0) -> bytes:
    """Create a fixed-size packet: header(6) + payload padded(248) + CRC32(4)."""
    if len(payload) > PAYLOAD_SIZE:
        raise ValueError("Payload máximo de 248 bytes")

    header = MAGIC + (seq % 65536).to_bytes(2, "big") + len(payload).to_bytes(2, "big")
    padded_payload = payload + b"\x00" * (PAYLOAD_SIZE - len(payload))
    data = header + padded_payload
    crc = zlib.crc32(data).to_bytes(CRC_SIZE, "big")
    return data + crc


def unpack(raw: bytes) -> tuple[int, bytes] | None:
    """Validate and unpack a packet.

    Returns:
        tuple(seq, payload) when valid, otherwise ``None``.
    """
    if len(raw) != PACKET_SIZE:
        return None

    header = raw[:HEADER_SIZE]
    if header[:2] != MAGIC:
        return None

    payload_len = int.from_bytes(header[4:6], "big")
    if payload_len > PAYLOAD_SIZE:
        return None

    payload = raw[HEADER_SIZE : HEADER_SIZE + payload_len]

    expected_crc = zlib.crc32(raw[:-CRC_SIZE]).to_bytes(CRC_SIZE, "big")
    if expected_crc != raw[-CRC_SIZE:]:
        return None

    seq = int.from_bytes(header[2:4], "big")
    return seq, payload
