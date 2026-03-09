"""Transmissão via saída de áudio."""

import numpy as np
import sounddevice as sd

from modem.modulator import SAMPLE_RATE

PREAMBLE_DURATION = 0.5  # segundos de tom de sincronismo


def _preamble() -> np.ndarray:
    t = np.linspace(0, PREAMBLE_DURATION, int(SAMPLE_RATE * PREAMBLE_DURATION))
    return np.sin(2 * np.pi * 1200 * t).astype(np.float32)


def transmit(signal: np.ndarray):
    full = np.concatenate([_preamble(), signal, _preamble()])
    sd.play(full, SAMPLE_RATE)
    sd.wait()
