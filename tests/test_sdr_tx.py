from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from sdr.sdr_tx import transmit


class FakeSoapy:
    SOAPY_SDR_TX = 0
    SOAPY_SDR_CF32 = 1


def test_transmit_configures_and_writes_stream():
    mock_sdr = MagicMock()
    mock_sdr.setupStream.return_value = "stream"
    mock_sdr.writeStream.return_value = SimpleNamespace(ret=2)

    fake_module = SimpleNamespace(
        Device=MagicMock(return_value=mock_sdr),
        SOAPY_SDR_TX=0,
        SOAPY_SDR_CF32=1,
    )

    with patch.dict("sys.modules", {"SoapySDR": fake_module}):
        transmit(np.array([1 + 0j, 0 + 1j], dtype=np.complex64), frequency_hz=100e6, sample_rate=1e6)

    mock_sdr.setSampleRate.assert_called_with(0, 0, 1e6)
    mock_sdr.setFrequency.assert_called_with(0, 0, 100e6)
    mock_sdr.activateStream.assert_called_once_with("stream")
    mock_sdr.writeStream.assert_called()
    mock_sdr.deactivateStream.assert_called_once_with("stream")
    mock_sdr.closeStream.assert_called_once_with("stream")


def test_transmit_invalid_frequency_raises():
    with pytest.raises(ValueError):
        transmit(np.array([0j], dtype=np.complex64), frequency_hz=0)
