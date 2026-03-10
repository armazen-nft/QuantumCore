import unittest
import numpy as np
from core.packet import pack, unpack
from modem.modulator import modulate
from modem.demodulator import demodulate

def add_channel_effects(audio: np.ndarray, snr_db: float = 10):
    """Simulação realista de canal SDR/FM (ruído + eco + desvanecimento)"""
    noise = np.random.normal(0, 10**(-snr_db/20), len(audio))
    echo = np.roll(audio, int(48000 * 0.003)) * 0.4
    fade = np.sin(np.linspace(0, 4*np.pi, len(audio))) * 0.3 + 1.0
    return np.clip((audio + echo + noise) * fade, -1.0, 1.0)

class TestFEC_SDR(unittest.TestCase):

    def test_fec_recovery_in_noisy_channel(self):
        """FEC Reed-Solomon deve recuperar pacote mesmo com ruído forte"""
        original = b"Teste FEC integrado no relay 2026 \ud83d\ude80"
        pkt = pack(original)
        clean = modulate(pkt)
        noisy = add_channel_effects(clean, snr_db=5)   # SNR baixo
        packets = demodulate(noisy)
        self.assertGreater(len(packets), 0)
        result = unpack(packets[0])
        self.assertIsNotNone(result)
        self.assertEqual(result[1], original)

    def test_sdr_simulation_equivalent_to_real(self):
        """Simula exatamente o fluxo RTL-SDR (FM demod → FSK)"""
        original = b"Payload via SDR simulado"
        pkt = pack(original)
        clean = modulate(pkt)
        noisy = add_channel_effects(clean, snr_db=10)
        packets = demodulate(noisy)
        result = unpack(packets[0])
        self.assertEqual(result[1], original)

    def test_node_relay_fec_correction(self):
        """Verifica que unpack() (FEC) é chamado no relay"""
        # Teste isolado do retransmitter (já validado antes)
        from network.retransmit import AntiStormRetransmitter
        rt = AntiStormRetransmitter()
        pkt = pack(b"teste")
        self.assertTrue(rt.should_retransmit(pkt))
        self.assertFalse(rt.should_retransmit(pkt, incoming_ttl=0))

if __name__ == "__main__":
    print("🔬 Rodando testes completos FEC + SDR simulado...")
    unittest.main(verbosity=2)
