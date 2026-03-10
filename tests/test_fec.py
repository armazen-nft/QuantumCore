import unittest

from core.fec import add_fec, remove_fec
from core.packet import pack, unpack


class TestFEC(unittest.TestCase):
    def test_fec_roundtrip(self):
        original = "Teste FEC com ruido 2026 🚀".encode("utf-8")
        with_fec = add_fec(original)
        recovered = remove_fec(with_fec)
        self.assertEqual(recovered, original)

    def test_fec_with_packet(self):
        data = b"Payload protegido por FEC"
        pkt = pack(add_fec(data))
        unpacked = unpack(pkt)
        self.assertIsNotNone(unpacked)
        assert unpacked is not None
        _, recovered = unpacked
        self.assertEqual(remove_fec(recovered), data)


if __name__ == "__main__":
    unittest.main(verbosity=2)
