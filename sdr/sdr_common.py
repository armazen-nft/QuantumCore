from __future__ import annotations

import numpy as np
from scipy import signal


def real_to_iq(samples: np.ndarray) -> np.ndarray:
    """Convert a real-valued baseband signal into complex IQ (imaginary=0)."""
    return samples.astype(np.float32).astype(np.complex64)


def resample_iq(iq_samples: np.ndarray, input_rate: int, output_rate: int) -> np.ndarray:
    """Resample IQ samples from input_rate to output_rate."""
    if input_rate <= 0 or output_rate <= 0:
        raise ValueError("Sample rates must be positive")
    target_size = int(len(iq_samples) * (output_rate / input_rate))
    if target_size <= 0:
        return np.array([], dtype=np.complex64)
    resampled = signal.resample(iq_samples, target_size)
    return resampled.astype(np.complex64)
