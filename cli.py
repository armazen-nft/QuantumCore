"""Command-line interface for OpenFM transmission modes."""

from __future__ import annotations

import argparse
from pathlib import Path

from audio.audio_rx import receive_audio
from audio.audio_tx import transmit_audio
from modem.modulator import modulate_fsk
from sdr.sdr_tx import transmit_sdr


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="OpenFM CLI")
    parser.add_argument("--mode", choices=["tx", "rx"], required=True)
    parser.add_argument("--input", help="File path for TX mode")
    parser.add_argument("--duration", type=float, default=5.0, help="RX capture duration")
    parser.add_argument("--backend", help="Audio backend override")
    parser.add_argument("--sdr", action="store_true", help="Use SDR transmitter")
    parser.add_argument("--freq", type=float, help="SDR carrier frequency in MHz")
    return parser


def main() -> None:
    args = build_parser().parse_args()

    if args.mode == "tx":
        if not args.input:
            raise SystemExit("--input is required for tx mode")
        payload = Path(args.input).read_bytes()
        samples = modulate_fsk(payload)
        if args.sdr:
            if args.freq is None:
                raise SystemExit("--freq is required when using --sdr")
            transmit_sdr(samples, frequency=args.freq * 1e6)
        else:
            transmit_audio(samples, backend=args.backend)
    else:
        receive_audio(duration=args.duration, backend=args.backend)


if __name__ == "__main__":
    main()
