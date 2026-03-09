"""Demodulação FSK por energia de banda."""

import numpy as np

SAMPLE_RATE = 44100
BAUD = 1200
BIT_SAMPLES = SAMPLE_RATE // BAUD
F0 = 1200.0
F1 = 2400.0

# vetores de correlação pré-calculados
_t = np.linspace(0, 1 / BAUD, BIT_SAMPLES, endpoint=False)
_C0 = np.exp(1j * 2 * np.pi * F0 * _t)
_C1 = np.exp(1j * 2 * np.pi * F1 * _t)


def demodulate(signal: np.ndarray) -> list[int]:
    bits = []
    for i in range(0, len(signal) - BIT_SAMPLES + 1, BIT_SAMPLES):
        seg = signal[i : i + BIT_SAMPLES]
        e0 = abs(np.dot(seg, _C0.conj()))
        e1 = abs(np.dot(seg, _C1.conj()))
        bits.append(1 if e1 > e0 else 0)
    return bits
