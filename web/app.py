import threading
import time
from queue import Queue

from flask import Flask, render_template_string

from audio.tx_rx import record
from core.packet import unpack
from modem.demodulator import demodulate

app = Flask(__name__)
log_queue: Queue = Queue()
received_packets = []

HTML = """
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>QuantumCore Monitor</title>
<style>body{font-family:monospace;background:#111;color:#0f0;padding:20px;}</style>
</head>
<body>
<h1>🚀 QuantumCore Network Monitor</h1>
<pre id="log">{{ log }}</pre>
<script>
function refresh() {
    fetch('/log').then(r => r.text()).then(txt => {
        document.getElementById('log').innerHTML = txt;
        setTimeout(refresh, 1000);
    });
}
refresh();
</script>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(HTML, log="\n".join(received_packets[-50:]))


@app.route("/log")
def log():
    return "\n".join(received_packets[-50:]) or "Aguardando pacotes..."


def background_rx():
    while True:
        try:
            audio = record(4.0)
            packets = demodulate(audio)
            for pkt in packets:
                result = unpack(pkt)
                if result:
                    seq, payload = result
                    msg = (
                        f"[{time.strftime('%H:%M:%S')}] Pacote {seq} recebido: "
                        f"{payload.decode(errors='ignore')[:120]}"
                    )
                    received_packets.append(msg)
                    log_queue.put(msg)
        except Exception:
            time.sleep(1)


if __name__ == "__main__":
    print("🌐 Iniciando QuantumCore Web Monitor http://127.0.0.1:5000")
    threading.Thread(target=background_rx, daemon=True).start()
    app.run(host="0.0.0.0", port=5000, debug=False)
