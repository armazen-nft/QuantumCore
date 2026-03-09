"""Modulação FSK: bit 0 → 1200 Hz · bit 1 → 2400 Hz."""

import numpy as np

SAMPLE_RATE = 44100
BAUD = 1200
BIT_SAMPLES = SAMPLE_RATE // BAUD  # 36 amostras por bit
F0 = 1200.0  # frequência para bit 0
F1 = 2400.0  # frequência para bit 1


def modulate(bits: list[int]) -> np.ndarray:
    t = np.linspace(0, 1 / BAUD, BIT_SAMPLES, endpoint=False)
    segments = [np.sin(2 * np.pi * (F1 if b else F0) * t) for b in bits]
    return np.concatenate(segments).astype(np.float32)
