"""Transmite um arquivo via FSK/áudio."""

import sys

from audio.audio_tx import transmit
from core.encoder import encode_file, packet_to_bits
from modem.modulator import modulate


def main():
    if len(sys.argv) < 2:
        print("uso: python send_file.py <arquivo>")
        sys.exit(1)

    path = sys.argv[1]
    packets = encode_file(path)
    print(f"[tx] {len(packets)} pacotes gerados")

    for i, pkt in enumerate(packets):
        bits = packet_to_bits(pkt)
        signal = modulate(bits)
        print(f"[tx] transmitindo pacote {i + 1}/{len(packets)} …")
        transmit(signal)

    print("[tx] concluído")


if __name__ == "__main__":
    main()
