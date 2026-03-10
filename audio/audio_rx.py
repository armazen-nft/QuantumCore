"""Receive waveform from configured audio backend."""

from __future__ import annotations

from audio.audio_bridge import create_audio_bridge


def receive_audio(duration: float, sample_rate: int = 48_000, backend: str | None = None):
    bridge = create_audio_bridge(backend=backend)
    return bridge.record(duration=duration, sample_rate=sample_rate)
