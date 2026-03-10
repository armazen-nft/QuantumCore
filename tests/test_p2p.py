import time
import unittest

from network.retransmit import AntiStormRetransmitter


class TestP2PAntiStorm(unittest.TestCase):
    def test_no_storm(self):
        rt = AntiStormRetransmitter(max_ttl=3)
        pkt = b"pacote-teste"
        self.assertTrue(rt.should_retransmit(pkt))
        self.assertTrue(rt.should_retransmit(pkt, incoming_ttl=2))
        self.assertFalse(rt.should_retransmit(pkt, incoming_ttl=0))

    def test_cache_timeout(self):
        rt = AntiStormRetransmitter(cache_timeout_sec=0.1)
        pkt = b"pacote-cache"
        rt.should_retransmit(pkt)
        time.sleep(0.2)
        self.assertTrue(rt.should_retransmit(pkt))


if __name__ == "__main__":
    unittest.main(verbosity=2)
