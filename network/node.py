"""Nó P2P: escuta, armazena e retransmite pacotes."""

import random
import time

from audio.audio_rx import record
from audio.audio_tx import transmit
from core.decoder import bits_to_bytes
from core.encoder import packet_to_bits
from core.packet import parse_packet
from modem.demodulator import demodulate
from modem.modulator import modulate

LISTEN_DURATION = 10  # segundos por ciclo de escuta
RETRANSMIT_WINDOW = 5  # jitter máximo antes de retransmitir

_seen: set[tuple] = set()
_store: list[bytes] = []


def _uid(pkt: dict) -> tuple:
    return (pkt["node_id"], pkt["packet_id"])


def run():
    print("[node] iniciando loop P2P…")
    while True:
        signal = record(LISTEN_DURATION)
        bits = demodulate(signal)
        raw = bits_to_bytes(bits)

        # divide em chunks de tamanho de pacote (heurístico)
        new_packets = []
        for i in range(0, len(raw), 271):  # 15 header + 256 payload
            pkt = parse_packet(raw[i:])
            if pkt and _uid(pkt) not in _seen:
                _seen.add(_uid(pkt))
                _store.append(raw[i : i + 271])
                new_packets.append(raw[i : i + 271])
                print(f"[node] pkt recebido: {_uid(pkt)}")

        if new_packets:
            time.sleep(random.uniform(0, RETRANSMIT_WINDOW))
            for pkt_bytes in new_packets:
                signal_out = modulate(packet_to_bits(pkt_bytes))
                transmit(signal_out)
                print(f"[node] retransmitido {len(pkt_bytes)} bytes")
