import numpy as np
import sounddevice as sd

from modem.modulator import SAMPLE_RATE  # reutiliza a configuração exata


def transmit(audio: np.ndarray, volume: float = 0.8):
    """Reproduz áudio (alto-falante ou rádio FM)"""
    audio = audio * volume
    print(f"▶️  Transmitindo {len(audio) / SAMPLE_RATE:.2f} segundos...")
    sd.play(audio, SAMPLE_RATE)
    sd.wait()
    print("✅ Transmissão finalizada")


def record(duration_seconds: float = 5.0) -> np.ndarray:
    """Grava do microfone (ou saída de rádio FM)"""
    print(f"🎤 Gravando por {duration_seconds} segundos... (fale ou ligue o rádio)")
    rec = sd.rec(
        int(duration_seconds * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32",
    )
    sd.wait()
    audio = rec.flatten()
    print(f"✅ Gravação finalizada ({len(audio)} amostras)")
    return audio
