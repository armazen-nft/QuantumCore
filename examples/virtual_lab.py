import numpy as np

from core.packet import pack, unpack
from modem.demodulator import demodulate
from modem.modulator import modulate


def add_channel_effects(audio: np.ndarray, snr_db: float = 10):
    noise = np.random.normal(0, 10 ** (-snr_db / 20), len(audio))
    echo = np.roll(audio, int(48000 * 0.003)) * 0.4
    fade = np.sin(np.linspace(0, 4 * np.pi, len(audio))) * 0.3 + 1.0
    return np.clip((audio + echo + noise) * fade, -1.0, 1.0)


print("🧪 Laboratório Virtual QuantumCore – FEC Reed-Solomon + Ruído\n")

data = "Teste FEC RS em canal ruidoso 2026 🚀📻".encode("utf-8")
for snr in [20, 10, 5, 0]:
    pkt = pack(data)
    clean = modulate(pkt)
    noisy = add_channel_effects(clean, snr_db=snr)

    packets = demodulate(noisy)
    success = False
    if packets:
        result = unpack(packets[0])
        if result and result[1] == data:
            success = True

    print(
        f"SNR = {snr:2d} dB → {'✅ RECUPERADO (FEC salvou!)' if success else '❌ Falhou (aumente RS ou reduza ruído)'}"
    )
