import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from audio.tx_rx import record, transmit
from core.packet import pack, unpack
from modem.demodulator import demodulate
from modem.modulator import modulate
from network.retransmit import AntiStormRetransmitter

retransmitter = AntiStormRetransmitter(max_ttl=5)


def main():
    parser = argparse.ArgumentParser(description="QuantumCore CLI - OpenFM P2P")
    parser.add_argument(
        "--mode",
        choices=["tx", "rx", "relay"],
        required=True,
        help="Modo: tx (enviar), rx (receber), relay (retransmitir)",
    )
    parser.add_argument("--file", type=str, help="Arquivo para enviar (modo tx)")
    parser.add_argument("--device", type=int, default=None, help="Índice de dispositivo")
    parser.add_argument(
        "--duration", type=float, default=8.0, help="Tempo de gravação no rx/relay"
    )
    args = parser.parse_args()

    if args.mode == "tx":
        if not args.file:
            print("❌ --file obrigatório no modo tx")
            sys.exit(1)
        with open(args.file, "rb") as f:
            data = f.read()
        print(f"📤 Enviando {len(data)} bytes...")
        pkt = pack(data)
        audio = modulate(pkt)
        transmit(audio, device=args.device)

    elif args.mode == "rx":
        print("🎤 Modo receptor...")
        audio = record(args.duration, device=args.device)
        packets = demodulate(audio)
        for pkt in packets:
            unpacked = unpack(pkt)
            if unpacked is not None:
                seq, payload = unpacked
                print(f"✅ Recebido seq={seq}: {payload.decode(errors='ignore')[:100]}...")

    elif args.mode == "relay":
        print("🔄 Modo Relay (P2P com anti-storm)...")
        while True:
            audio = record(args.duration, device=args.device)
            packets = demodulate(audio)
            for pkt in packets:
                if retransmitter.should_retransmit(pkt):
                    print("🔁 Retransmitindo pacote...")
                    retransmitter.cleanup()
                    audio_out = modulate(pkt)
                    transmit(audio_out, device=args.device)


if __name__ == "__main__":
    main()
