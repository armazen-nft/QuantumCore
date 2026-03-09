"""Recebe pacotes via áudio e reconstrói o arquivo."""

import sys

from audio.audio_rx import record
from core.decoder import bits_to_bytes, decode_packets
from core.packet import parse_packet
from modem.demodulator import demodulate

DURATION = 60  # segundos de escuta
OUTPUT_PATH = "received_output.bin"


def main():
    print(f"[rx] escutando por {DURATION}s …")
    signal = record(DURATION)
    bits = demodulate(signal)
    raw = bits_to_bytes(bits)

    # coleta todos os pacotes válidos do stream
    raw_packets = []
    pkt_size = 271
    for i in range(0, len(raw) - pkt_size + 1, pkt_size):
        chunk = raw[i : i + pkt_size]
        if parse_packet(chunk):
            raw_packets.append(chunk)

    print(f"[rx] {len(raw_packets)} pacotes válidos")
    data = decode_packets(raw_packets)

    if data is None:
        print("[rx] falha na reconstrução (pacotes insuficientes)")
        sys.exit(1)

    with open(OUTPUT_PATH, "wb") as f:
        f.write(data)
    print(f"[rx] arquivo salvo em {OUTPUT_PATH} ({len(data)} bytes)")


if __name__ == "__main__":
    main()
