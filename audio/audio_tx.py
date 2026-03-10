from __future__ import annotations

import numpy as np

from .audio_bridge import AudioIO


def transmit_audio(samples: np.ndarray, samplerate: int = 48_000, backend: str | None = None) -> None:
    audio = AudioIO.get_instance(backend=backend)
    audio.play(samples=samples, samplerate=samplerate, blocking=True)
