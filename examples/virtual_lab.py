import math
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.packet import pack, unpack
from modem.demodulator import demodulate
from modem.modulator import modulate


def add_channel_effects(audio, snr_db: float = 10):
    """Simula canal FM (ruído, eco, desvanecimento) sem dependências externas."""
    noise_sigma = 10 ** (-snr_db / 20)
    delay = int(48_000 * 0.002)
    out = []
    n = len(audio)
    for i, sample in enumerate(audio):
        echo = audio[i - delay] * 0.3 if i - delay >= 0 else 0.0
        fade = math.sin((2 * math.pi * i) / max(1, n - 1)) * 0.2 + 1.0
        noise = random.gauss(0, noise_sigma)
        out.append((sample + echo + noise) * fade)
    return out


def main():
    data = b"Laboratorio Virtual QuantumCore 2026 - Teste de ruido forte!"
    pkt = pack(data)
    clean_audio = modulate(pkt)

    print("🧪 Laboratório Virtual QuantumCore")
    for snr in [20, 10, 5, 0]:
        noisy = add_channel_effects(clean_audio, snr_db=snr)
        packets = demodulate(noisy)
        success = False
        if packets:
            unpacked = unpack(packets[0])
            success = unpacked is not None and unpacked[1] == data
        print(f"SNR = {snr} dB → {'✅ Sucesso' if success else '❌ Falha'} (FEC ajudaria aqui!)")


if __name__ == "__main__":
    main()
