from __future__ import annotations

import threading
import time
from flask import Flask, jsonify, render_template

from network.node import get_peer_list

app = Flask(__name__)
peer_cache: list[dict] = []
last_update: float = 0.0


def update_peers_loop() -> None:
    global peer_cache, last_update
    while True:
        peer_cache = get_peer_list()
        last_update = time.time()
        time.sleep(10)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/peers")
def api_peers():
    return jsonify({"peers": peer_cache, "last_update": last_update})


def start_background_updater() -> None:
    thread = threading.Thread(target=update_peers_loop, daemon=True)
    thread.start()


start_background_updater()
