"""Transmit waveform through configured audio backend."""

from __future__ import annotations

from audio.audio_bridge import create_audio_bridge


def transmit_audio(samples, sample_rate: int = 48_000, backend: str | None = None) -> None:
    bridge = create_audio_bridge(backend=backend)
    bridge.playback(samples, sample_rate=sample_rate)
