import argparse
import sys
from core.packet import pack, unpack
from modem.modulator import modulate
from audio.tx_rx import transmit, record
from modem.demodulator import demodulate
from network.node import QuantumNode

def main():
    parser = argparse.ArgumentParser(description="🚀 QuantumCore CLI - OpenFM P2P com FEC + SDR")
    parser.add_argument("--mode", choices=["tx", "rx", "relay"], required=True,
                        help="Modo: tx (enviar), rx (receber), relay (retransmitir com FEC)")
    parser.add_argument("--file", type=str, help="Arquivo para enviar (modo tx)")
    parser.add_argument("--duration", type=float, default=8.0, help="Tempo de gravação (rx/relay)")
    parser.add_argument("--sdr", action="store_true", help="Usar RTL-SDR para RX/Relay")
    parser.add_argument("--freq", type=float, default=87.5, help="Frequência MHz do SDR")
    args = parser.parse_args()

    if args.mode == "tx":
        if not args.file:
            print("❌ --file obrigatório no modo tx")
            sys.exit(1)
        with open(args.file, "rb") as f:
            data = f.read()
        print(f"📤 Enviando {len(data)} bytes (com FEC)...")
        pkt = pack(data)
        audio = modulate(pkt)
        transmit(audio)

    elif args.mode == "rx":
        print(f"🎤 Modo receptor {'(SDR)' if args.sdr else '(áudio)'}...")
        if args.sdr:
            from sdr.sdr_rx import sdr_record
            audio = sdr_record(args.duration, args.freq)
        else:
            audio = record(args.duration)
        packets = demodulate(audio)
        for pkt in packets:
            result = unpack(pkt)  # FEC corrige erros automaticamente
            if result:
                seq, payload = result
                print(f"✅ Recebido {seq}: {payload.decode(errors='ignore')[:100]}...")

    elif args.mode == "relay":
        print("🔄 Iniciando QuantumNode Relay (FEC + Anti-Storm)...")
        node = QuantumNode()
        node.relay(args.duration, args.sdr, args.freq)

if __name__ == "__main__":
    main()
