"""Desktop audio backend using SoundDevice/PortAudio."""

from __future__ import annotations

import numpy as np


class SoundDeviceAudioIO:
    def __init__(self) -> None:
        try:
            import sounddevice as sd
        except ImportError as exc:
            raise RuntimeError("sounddevice is required for desktop backend") from exc
        self._sd = sd

    def record(self, duration: float, sample_rate: int = 48_000) -> np.ndarray:
        frames = int(duration * sample_rate)
        samples = self._sd.rec(frames, samplerate=sample_rate, channels=1, dtype="float32")
        self._sd.wait()
        return samples[:, 0]

    def playback(self, samples, sample_rate: int = 48_000) -> None:
        mono = np.asarray(samples, dtype=np.float32)
        self._sd.play(mono, samplerate=sample_rate)
        self._sd.wait()
