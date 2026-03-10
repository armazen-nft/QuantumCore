"""Run a simple P2P node with optional web monitor."""

from __future__ import annotations

import argparse

from network.node import Node
from web_monitor.app import create_app


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--node-id", default="node-local")
    parser.add_argument("--web-monitor", action="store_true")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()

    node = Node(node_id=args.node_id)
    node.peer_discovery.upsert_peer(node_id=args.node_id, ip="127.0.0.1", stored_packets=0)

    if args.web_monitor:
        app = create_app(node)
        app.run(host=args.host, port=args.port)


if __name__ == "__main__":
    main()
