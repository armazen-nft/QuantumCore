import hashlib
import time


class AntiStormRetransmitter:
    """Evita retransmissões em tempestade com TTL e cache de vistos."""

    def __init__(self, max_ttl: int = 5, cache_timeout_sec: int = 300):
        self.max_ttl = max_ttl
        self.cache_timeout = cache_timeout_sec
        self.seen: dict[str, tuple[float, int]] = {}

    def _hash(self, packet: bytes) -> str:
        return hashlib.sha256(packet).hexdigest()

    def should_retransmit(self, packet: bytes, incoming_ttl: int | None = None) -> bool:
        pkt_hash = self._hash(packet)
        now = time.time()

        if pkt_hash in self.seen:
            expiry, remaining = self.seen[pkt_hash]
            if now < expiry and remaining <= 0:
                return False

        ttl = incoming_ttl if incoming_ttl is not None else self.max_ttl
        self.seen[pkt_hash] = (now + self.cache_timeout, ttl - 1)
        return ttl > 0

    def cleanup(self):
        now = time.time()
        expired = [h for h, (exp, _) in self.seen.items() if now > exp]
        for h in expired:
            del self.seen[h]
