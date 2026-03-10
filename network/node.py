from .retransmit import AntiStormRetransmitter
from core.packet import unpack, pack
from modem.demodulator import demodulate
from modem.modulator import modulate
from audio.tx_rx import transmit, record

class QuantumNode:
    """Nó P2P completo: corrige com FEC antes de retransmitir (anti-storm)"""
    def __init__(self):
        self.retransmitter = AntiStormRetransmitter(max_ttl=5)

    def relay(self, duration: float = 8.0, use_sdr: bool = False, freq_mhz: float = 87.5):
        print("🔄 QuantumNode Relay (FEC Reed-Solomon + Anti-Storm) iniciado")
        while True:
            # Escolha de fonte de áudio
            if use_sdr:
                try:
                    from sdr.sdr_rx import sdr_record
                    audio = sdr_record(duration, freq_mhz)
                except ImportError:
                    print("❌ RTL-SDR não instalado. Use modo áudio.")
                    return
            else:
                audio = record(duration)

            packets = demodulate(audio)
            for pkt in packets:
                result = unpack(pkt)  # ← FEC corrige erros aqui!
                if result:
                    seq, payload = result
                    print(f"✅ Pacote {seq} corrigido por FEC → retransmitindo")

                    if self.retransmitter.should_retransmit(pkt):
                        # Reempacota (mantém FEC atualizado)
                        new_pkt = pack(payload, seq=seq + 1)
                        audio_out = modulate(new_pkt)
                        transmit(audio_out)

                self.retransmitter.cleanup()
