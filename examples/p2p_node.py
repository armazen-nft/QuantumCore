"""Inicia um nó P2P completo (RF + LAN)."""

from core.packet import NODE_ID
from network.node import run as run_node
from network.peer_discovery import start as start_discovery


def main():
    print(f"[p2p] NODE_ID = {NODE_ID:#010x}")
    start_discovery(NODE_ID)
    run_node()


if __name__ == "__main__":
    main()
