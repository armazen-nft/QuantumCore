"""SDR transmission entrypoint."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

import numpy as np


class SDRBackend(Protocol):
    def send(self, iq_samples: np.ndarray, frequency: float, sample_rate: int) -> None:
        ...


@dataclass
class NullSDRBackend:
    """Default no-op backend to keep SDR plumbing testable without hardware."""

    sent: int = 0

    def send(self, iq_samples: np.ndarray, frequency: float, sample_rate: int) -> None:
        self.sent += len(iq_samples)


def _validate_frequency(frequency: float) -> None:
    # Broadly compatible range across common SDR transmitters.
    if frequency < 24e6 or frequency > 6e9:
        raise ValueError("frequency must be between 24 MHz and 6 GHz")


def to_iq(audio_samples: np.ndarray) -> np.ndarray:
    real = np.asarray(audio_samples, dtype=np.float32)
    imag = np.zeros_like(real)
    return (real + 1j * imag).astype(np.complex64)


def transmit_sdr(
    samples,
    frequency: float,
    sample_rate: int = 48_000,
    backend: SDRBackend | None = None,
) -> np.ndarray:
    _validate_frequency(frequency)
    iq = to_iq(np.asarray(samples, dtype=np.float32))
    (backend or NullSDRBackend()).send(iq, frequency=frequency, sample_rate=sample_rate)
    return iq
