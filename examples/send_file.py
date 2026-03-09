import os
import sys

from audio.tx_rx import transmit
from core.packet import pack
from modem.modulator import modulate

if len(sys.argv) < 2:
    print("Uso: python examples/send_file.py <arquivo>")
    sys.exit(1)

file_path = sys.argv[1]
if not os.path.exists(file_path):
    print("Arquivo não encontrado!")
    sys.exit(1)

with open(file_path, "rb") as f:
    data = f.read()

chunk_size = 248
total_packets = (len(data) + chunk_size - 1) // chunk_size

print(f"📤 Enviando {len(data)} bytes em {total_packets} pacotes...")

for i in range(0, len(data), chunk_size):
    chunk = data[i : i + chunk_size]
    seq = i // chunk_size
    pkt = pack(chunk, seq=seq)
    audio = modulate(pkt)
    transmit(audio)

print("🎉 Arquivo enviado com sucesso!")
