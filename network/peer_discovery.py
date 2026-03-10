"""In-memory peer registry for local node monitoring."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from threading import Lock
from time import time


@dataclass
class Peer:
    node_id: str
    ip: str
    stored_packets: int = 0
    last_seen: float = 0.0


class PeerDiscovery:
    def __init__(self) -> None:
        self._lock = Lock()
        self._peers: dict[str, Peer] = {}

    def upsert_peer(self, node_id: str, ip: str, stored_packets: int = 0) -> None:
        with self._lock:
            self._peers[node_id] = Peer(
                node_id=node_id,
                ip=ip,
                stored_packets=stored_packets,
                last_seen=time(),
            )

    def list_peers(self) -> list[dict]:
        with self._lock:
            return [asdict(peer) for peer in self._peers.values()]
