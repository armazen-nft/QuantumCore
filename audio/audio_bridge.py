"""Cross-platform audio bridge abstraction."""

from __future__ import annotations

import platform
from abc import ABC, abstractmethod
from typing import Optional

from audio.backends.android_backend import AndroidAudioIO
from audio.backends.ios_backend import IOSAudioIO
from audio.backends.sounddevice_backend import SoundDeviceAudioIO


class AudioIO(ABC):
    @abstractmethod
    def record(self, duration: float, sample_rate: int = 48_000):
        raise NotImplementedError

    @abstractmethod
    def playback(self, samples, sample_rate: int = 48_000) -> None:
        raise NotImplementedError


def create_audio_bridge(backend: Optional[str] = None) -> AudioIO:
    target = (backend or platform.system()).lower()

    if target in {"linux", "windows", "sounddevice"}:
        return SoundDeviceAudioIO()
    if target in {"android"}:
        return AndroidAudioIO()
    if target in {"ios", "darwin-ios"}:
        return IOSAudioIO()

    raise ValueError(f"Unsupported backend: {target}")
