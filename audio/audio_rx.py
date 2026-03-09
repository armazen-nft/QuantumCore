"""Captura de áudio para recepção."""

import numpy as np
import sounddevice as sd

from modem.modulator import SAMPLE_RATE


def record(duration: float) -> np.ndarray:
    audio = sd.rec(
        int(duration * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32",
    )
    sd.wait()
    return audio.flatten()
