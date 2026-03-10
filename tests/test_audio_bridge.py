from __future__ import annotations

from unittest.mock import MagicMock, patch

import numpy as np

from audio.audio_bridge import AudioIO, SoundDeviceAudioIO


def test_get_instance_returns_sounddevice_on_linux():
    with patch("audio.audio_bridge.platform.system", return_value="Linux"):
        instance = AudioIO.get_instance()
    assert isinstance(instance, SoundDeviceAudioIO)


def test_sounddevice_play_invokes_backend():
    with patch("sounddevice.play") as mock_play:
        backend = SoundDeviceAudioIO()
        backend.play(np.array([0.0, 0.1], dtype=np.float32), samplerate=48_000)
    mock_play.assert_called_once()


def test_sounddevice_record_flattens_data():
    fake = np.array([[0.1], [0.2]], dtype=np.float32)
    with patch("sounddevice.rec", return_value=fake) as mock_rec, patch("sounddevice.wait"):
        backend = SoundDeviceAudioIO()
        recorded = backend.record(duration=2 / 48_000, samplerate=48_000)
    assert recorded.shape == (2,)
    mock_rec.assert_called_once()
