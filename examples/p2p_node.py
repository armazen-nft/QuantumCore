from __future__ import annotations

import argparse
import threading
import time

from web_monitor.app import app


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a simple P2P node loop")
    parser.add_argument("--web-monitor", action="store_true", help="Start web monitor")
    parser.add_argument("--port", type=int, default=5000)
    args = parser.parse_args()

    if args.web_monitor:
        thread = threading.Thread(
            target=app.run,
            kwargs={"host": "0.0.0.0", "port": args.port, "debug": False},
            daemon=True,
        )
        thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        return


if __name__ == "__main__":
    main()
