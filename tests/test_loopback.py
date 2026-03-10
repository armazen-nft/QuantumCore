import random
import unittest

from core.packet import pack, unpack
from modem.demodulator import demodulate
from modem.modulator import modulate


class TestQuantumCore(unittest.TestCase):
    def test_packet_crc(self):
        data = "Teste de integridade 2026 🚀".encode("utf-8")
        pkt = pack(data, seq=123)
        result = unpack(pkt)
        self.assertIsNotNone(result)
        assert result is not None
        self.assertEqual(result[1], data)

    def test_modem_loopback_synthetic(self):
        payload = b"Loopback sintetico QuantumCore"
        pkt = pack(payload)
        audio = modulate(pkt)
        packets = demodulate(audio)
        self.assertGreater(len(packets), 0)
        unpacked = unpack(packets[0])
        self.assertIsNotNone(unpacked)
        assert unpacked is not None
        _, rec = unpacked
        self.assertEqual(rec, payload)

    def test_full_loopback_with_noise(self):
        data = b"Teste com ruido real"
        pkt = pack(data)
        audio = modulate(pkt)

        noisy_audio = []
        for sample in audio:
            noise = random.gauss(0, 0.05)
            noisy_audio.append(max(-1.0, min(1.0, sample + noise)))

        packets = demodulate(noisy_audio)
        self.assertGreater(len(packets), 0)
        unpacked = unpack(packets[0])
        self.assertIsNotNone(unpacked)
        assert unpacked is not None
        _, rec = unpacked
        self.assertEqual(rec, data)


if __name__ == "__main__":
    print("🔬 Rodando testes automatizados do QuantumCore...")
    unittest.main(verbosity=2)
