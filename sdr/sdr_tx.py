from __future__ import annotations

import numpy as np


def transmit(
    samples: np.ndarray,
    frequency_hz: float,
    sample_rate: float = 1e6,
    gain: float = 0.0,
    device_args: str = "",
) -> None:
    if frequency_hz <= 0:
        raise ValueError("frequency_hz must be positive")
    if sample_rate <= 0:
        raise ValueError("sample_rate must be positive")

    import SoapySDR
    from SoapySDR import SOAPY_SDR_CF32, SOAPY_SDR_TX

    sdr = SoapySDR.Device(device_args)
    sdr.setSampleRate(SOAPY_SDR_TX, 0, sample_rate)
    sdr.setFrequency(SOAPY_SDR_TX, 0, frequency_hz)
    sdr.setGain(SOAPY_SDR_TX, 0, gain)

    stream = sdr.setupStream(SOAPY_SDR_TX, SOAPY_SDR_CF32, [0])
    sdr.activateStream(stream)

    chunk_size = 1024
    data = samples.astype(np.complex64)
    for start in range(0, len(data), chunk_size):
        chunk = data[start : start + chunk_size]
        result = sdr.writeStream(stream, [chunk], chunk.size, timeoutUs=1_000_000)
        if result.ret != chunk.size:
            raise RuntimeError(f"Short SDR write: wrote {result.ret}, expected {chunk.size}")

    sdr.deactivateStream(stream)
    sdr.closeStream(stream)
