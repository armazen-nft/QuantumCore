from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

from audio.audio_tx import transmit_audio
from sdr.sdr_common import real_to_iq, resample_iq
from sdr.sdr_tx import transmit as sdr_transmit


def modulate_bytes_as_fsk_like_audio(payload: bytes, samplerate: int = 48_000) -> np.ndarray:
    """Minimal placeholder to generate a waveform from bytes for demo/CLI integration."""
    if not payload:
        return np.array([], dtype=np.float32)
    bits = np.unpackbits(np.frombuffer(payload, dtype=np.uint8))
    tone0 = np.sin(2 * np.pi * 1200 * np.arange(0, 0.01, 1 / samplerate))
    tone1 = np.sin(2 * np.pi * 2400 * np.arange(0, 0.01, 1 / samplerate))
    chunks = [tone1 if bit else tone0 for bit in bits]
    return np.concatenate(chunks).astype(np.float32)


def main() -> None:
    parser = argparse.ArgumentParser(description="Transmit a file via audio or SDR")
    parser.add_argument("input_file")
    parser.add_argument("--mode", choices=["audio", "sdr"], default="audio")
    parser.add_argument("--freq", type=float, help="Frequency in MHz (required for SDR mode)")
    parser.add_argument("--backend", choices=["sounddevice", "android", "ios"], help="Audio backend")
    parser.add_argument("--sdr-sample-rate", type=float, default=1e6)
    args = parser.parse_args()

    payload = Path(args.input_file).read_bytes()
    audio_samples = modulate_bytes_as_fsk_like_audio(payload)

    if args.mode == "audio":
        transmit_audio(audio_samples, backend=args.backend)
        return

    if args.freq is None:
        parser.error("--freq is required in SDR mode")

    iq = real_to_iq(audio_samples)
    iq_resampled = resample_iq(iq, input_rate=48_000, output_rate=int(args.sdr_sample_rate))
    sdr_transmit(iq_resampled, frequency_hz=args.freq * 1e6, sample_rate=args.sdr_sample_rate)


if __name__ == "__main__":
    main()
