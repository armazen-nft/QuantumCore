"""Basic P2P node state."""

from __future__ import annotations

from dataclasses import dataclass, field

from network.peer_discovery import PeerDiscovery


@dataclass
class Node:
    node_id: str
    peer_discovery: PeerDiscovery = field(default_factory=PeerDiscovery)

    def known_peers(self) -> list[dict]:
        return self.peer_discovery.list_peers()
