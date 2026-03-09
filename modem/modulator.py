"""Simple FSK modulator for QuantumCore packets."""

from __future__ import annotations

import numpy as np

# FSK settings (FM-radio/audio-friendly)
SAMPLE_RATE = 48_000
BAUD_RATE = 1_200
SAMPLES_PER_BIT = SAMPLE_RATE // BAUD_RATE
MARK_FREQ = 1_200.0  # bit 1
SPACE_FREQ = 2_400.0  # bit 0


def modulate(packet: bytes) -> np.ndarray:
    """Modulate packet bytes into 1200-baud FSK audio with a sync preamble."""
    bits: list[int] = []
    for byte in packet:
        for i in range(8):
            bits.append((byte >> i) & 1)

    preamble = [1, 0] * 16  # 32 alternating bits for future demod sync
    all_bits = preamble + bits

    total_samples = len(all_bits) * SAMPLES_PER_BIT
    audio = np.zeros(total_samples, dtype=np.float32)

    index = 0
    t = np.arange(SAMPLES_PER_BIT) / SAMPLE_RATE
    for bit in all_bits:
        freq = MARK_FREQ if bit == 1 else SPACE_FREQ
        tone = np.sin(2 * np.pi * freq * t)
        audio[index : index + SAMPLES_PER_BIT] = tone
        index += SAMPLES_PER_BIT

    audio = audio / (np.max(np.abs(audio)) + 1e-8)
    return audio
