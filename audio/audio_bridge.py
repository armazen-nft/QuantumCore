from __future__ import annotations

from abc import ABC, abstractmethod
import platform
from typing import Any

import numpy as np


class AudioIO(ABC):
    """Cross-platform audio abstraction for playback/recording."""

    @abstractmethod
    def play(self, samples: np.ndarray, samplerate: int, blocking: bool = True) -> None:
        """Play audio samples."""

    @abstractmethod
    def record(self, duration: float, samplerate: int) -> np.ndarray:
        """Record audio for the provided duration in seconds."""

    @abstractmethod
    def get_devices(self) -> Any:
        """List available audio devices for the backend."""

    @classmethod
    def get_instance(cls, backend: str | None = None) -> "AudioIO":
        if backend:
            key = backend.strip().lower()
            if key in {"sounddevice", "linux", "windows"}:
                return SoundDeviceAudioIO()
            if key == "android":
                return AndroidAudioIO()
            if key in {"ios", "darwin"}:
                return IOSAudioIO()
            raise ValueError(f"Unsupported audio backend: {backend}")

        system = platform.system().lower()
        platform_name = platform.platform().lower()
        if system in {"linux", "windows"}:
            return SoundDeviceAudioIO()
        if "android" in platform_name:
            return AndroidAudioIO()
        if system == "darwin":
            return IOSAudioIO()
        raise RuntimeError(f"Unsupported platform: {system}")


class SoundDeviceAudioIO(AudioIO):
    def play(self, samples: np.ndarray, samplerate: int, blocking: bool = True) -> None:
        import sounddevice as sd

        sd.play(samples, samplerate=samplerate, blocking=blocking)

    def record(self, duration: float, samplerate: int) -> np.ndarray:
        import sounddevice as sd

        frames = int(duration * samplerate)
        recording = sd.rec(frames, samplerate=samplerate, channels=1)
        sd.wait()
        return recording.flatten()

    def get_devices(self) -> Any:
        import sounddevice as sd

        return sd.query_devices()


class AndroidAudioIO(AudioIO):
    def play(self, samples: np.ndarray, samplerate: int, blocking: bool = True) -> None:
        from jnius import autoclass
        import time

        AudioFormat = autoclass("android.media.AudioFormat")
        AudioTrack = autoclass("android.media.AudioTrack")

        pcm = np.clip(samples, -1.0, 1.0)
        pcm = (pcm * 32767).astype(np.int16).tobytes()
        min_size = AudioTrack.getMinBufferSize(
            samplerate,
            AudioFormat.CHANNEL_OUT_MONO,
            AudioFormat.ENCODING_PCM_16BIT,
        )
        track = AudioTrack(
            AudioTrack.STREAM_MUSIC,
            samplerate,
            AudioFormat.CHANNEL_OUT_MONO,
            AudioFormat.ENCODING_PCM_16BIT,
            max(min_size, len(pcm)),
            AudioTrack.MODE_STREAM,
        )
        track.play()
        track.write(pcm, 0, len(pcm))
        if blocking:
            time.sleep(len(samples) / samplerate)
        track.stop()
        track.release()

    def record(self, duration: float, samplerate: int) -> np.ndarray:
        raise NotImplementedError("Android recording backend is not implemented yet.")

    def get_devices(self) -> list[str]:
        return ["android-default-output", "android-default-input"]


class IOSAudioIO(AudioIO):
    def play(self, samples: np.ndarray, samplerate: int, blocking: bool = True) -> None:
        raise NotImplementedError("iOS playback backend requires platform bridge implementation.")

    def record(self, duration: float, samplerate: int) -> np.ndarray:
        raise NotImplementedError("iOS recording backend requires platform bridge implementation.")

    def get_devices(self) -> list[str]:
        return ["ios-default-audio"]
