"""
Descoberta de peers via broadcast UDP (LAN).
Complementa a camada RF para redes locais.
"""

import json
import socket
import threading
import time

PORT = 50700
INTERVAL = 10
_peers: set[str] = set()


def _beacon(node_id: int):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    msg = json.dumps({"node_id": node_id}).encode()
    while True:
        sock.sendto(msg, ("<broadcast>", PORT))
        time.sleep(INTERVAL)


def _listen():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", PORT))
    while True:
        data, addr = sock.recvfrom(256)
        try:
            json.loads(data)
            _peers.add(addr[0])
        except Exception:
            pass


def start(node_id: int):
    threading.Thread(target=_beacon, args=(node_id,), daemon=True).start()
    threading.Thread(target=_listen, daemon=True).start()


def get_peers() -> list[str]:
    return list(_peers)
