from __future__ import annotations

import random
import time
from dataclasses import dataclass, asdict


@dataclass
class Peer:
    id: str
    ip: str
    packets: int
    last_seen: float


def get_peer_list() -> list[dict]:
    now = time.time()
    peers = [
        Peer(id="node-a", ip="192.168.1.10", packets=random.randint(10, 80), last_seen=now - 5),
        Peer(id="node-b", ip="192.168.1.11", packets=random.randint(5, 40), last_seen=now - 11),
    ]
    return [asdict(peer) for peer in peers]
