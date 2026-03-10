"""FSK modulator utilities."""

from __future__ import annotations

import numpy as np


def modulate_fsk(
    data: bytes,
    baud_rate: int = 1200,
    sample_rate: int = 48_000,
    mark_freq: float = 1200.0,
    space_freq: float = 2200.0,
) -> np.ndarray:
    """Convert a bytes payload into a mono BFSK waveform.

    Returns float32 samples in [-1, 1].
    """
    if baud_rate <= 0 or sample_rate <= 0:
        raise ValueError("baud_rate and sample_rate must be positive")

    bits = np.unpackbits(np.frombuffer(data, dtype=np.uint8))
    if bits.size == 0:
        return np.array([], dtype=np.float32)

    samples_per_bit = max(1, int(sample_rate / baud_rate))
    total_samples = bits.size * samples_per_bit
    t = np.arange(total_samples, dtype=np.float32) / sample_rate

    bit_expanded = np.repeat(bits, samples_per_bit)
    freqs = np.where(bit_expanded == 1, mark_freq, space_freq).astype(np.float32)
    phase = 2.0 * np.pi * np.cumsum(freqs) / sample_rate
    waveform = 0.5 * np.sin(phase)
    return waveform.astype(np.float32)
