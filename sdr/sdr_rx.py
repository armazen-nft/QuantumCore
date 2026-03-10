import numpy as np
from rtlsdr import RtlSdr
from scipy.signal import resample

from core.packet import unpack
from modem.demodulator import demodulate

SAMPLE_RATE = 48000


def sdr_record(
    duration_seconds: float = 5.0, freq_mhz: float = 87.5, gain_db: int = 20
) -> np.ndarray:
    """RTL-SDR → Demodulação FM → Áudio 48kHz pronto para FSK"""
    sdr = RtlSdr()
    sdr.sample_rate = 2.048e6
    sdr.center_freq = freq_mhz * 1e6
    sdr.gain = gain_db
    sdr.set_agc_mode(True)

    print(
        f"📡 RTL-SDR sintonizado em {freq_mhz} MHz (ganho {gain_db}dB) - gravando {duration_seconds}s..."
    )

    num_samples = int(duration_seconds * sdr.sample_rate)
    iq = sdr.read_samples(num_samples)
    sdr.close()

    # Demodulação FM (derivada da fase)
    phase = np.unwrap(np.angle(iq))
    demod = np.diff(phase)

    # Normaliza e resample para 48kHz (compatível com demodulador FSK)
    audio = demod / (np.max(np.abs(demod)) + 1e-8)
    audio = resample(audio, int(len(audio) * SAMPLE_RATE / sdr.sample_rate))
    audio = audio.astype(np.float32)

    print(f"✅ SDR pronto ({len(audio)} amostras @ 48kHz)")
    return audio


# Exemplo rápido de uso (pode integrar no cli.py depois)
if __name__ == "__main__":
    audio = sdr_record(6.0, freq_mhz=87.5)
    packets = demodulate(audio)
    for pkt in packets:
        result = unpack(pkt)
        if result:
            seq, payload = result
            print(f"✅ Pacote {seq} recebido via SDR: {payload.decode(errors='ignore')[:100]}")
