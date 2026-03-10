"""Simple Flask web monitor for active peers."""

from __future__ import annotations

from flask import Flask, jsonify, send_from_directory

from network.node import Node


def create_app(node: Node) -> Flask:
    app = Flask(__name__, static_folder="static")

    @app.get("/api/peers")
    def peers_api():
        return jsonify(node.known_peers())

    @app.get("/")
    def index():
        return send_from_directory(app.static_folder, "index.html")

    return app
