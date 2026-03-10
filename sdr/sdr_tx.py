import os
import subprocess

import numpy as np

from core.packet import pack
from modem.modulator import modulate

SAMPLE_RATE = 2048000  # HackRF suporta


def audio_to_iq(audio: np.ndarray) -> np.ndarray:
    """Converte FSK áudio em IQ FM (baseband) para transmissão direta."""
    deviation = 75000.0  # 75 kHz (padrão FM)
    phase = 2 * np.pi * deviation * np.cumsum(audio) / SAMPLE_RATE
    iq = np.exp(1j * phase).astype(np.complex64)
    return iq


def scale_to_int8(iq: np.ndarray) -> np.ndarray:
    """Converte complex64 → interleaved signed 8-bit (formato do hackrf_transfer)."""
    iq_scaled = np.clip(iq * 127, -127, 127)
    iq_int8 = np.empty(len(iq) * 2, dtype=np.int8)
    iq_int8[0::2] = np.real(iq_scaled).astype(np.int8)
    iq_int8[1::2] = np.imag(iq_scaled).astype(np.int8)
    return iq_int8


def transmit_sdr(payload: bytes, freq_mhz: float = 87.5, gain_db: int = 40):
    """Transmite pacote direto na frequência via HackRF."""
    pkt = pack(payload)
    audio = modulate(pkt)
    iq = audio_to_iq(audio)
    iq_int8 = scale_to_int8(iq)

    iq_file = "tx.iq"
    with open(iq_file, "wb") as f:
        f.write(iq_int8.tobytes())

    print(f"📡 Transmitindo {len(payload)} bytes em {freq_mhz} MHz (HackRF TX)...")

    cmd = [
        "hackrf_transfer",
        "-t",
        iq_file,
        "-f",
        str(int(freq_mhz * 1_000_000)),
        "-s",
        str(SAMPLE_RATE),
        "-x",
        str(gain_db),
        "-a",
        "1",
    ]

    try:
        subprocess.run(cmd, check=True, timeout=30)
        print("✅ Transmissão SDR finalizada")
    except FileNotFoundError:
        print("❌ hackrf_transfer não encontrado! Instale hackrf-tools.")
    except Exception as e:
        print(f"Erro TX: {e}")
    finally:
        if os.path.exists(iq_file):
            os.remove(iq_file)


if __name__ == "__main__":
    transmit_sdr("Teste SDR TX direto 2026 🚀".encode("utf-8"), freq_mhz=87.5, gain_db=47)
