from __future__ import annotations

import numpy as np

from .audio_bridge import AudioIO


def receive_audio(duration: float, samplerate: int = 48_000, backend: str | None = None) -> np.ndarray:
    audio = AudioIO.get_instance(backend=backend)
    return audio.record(duration=duration, samplerate=samplerate)
