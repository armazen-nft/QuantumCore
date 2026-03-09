#!/usr/bin/env python3
"""
recreate.py — gera a estrutura completa do QuantumCore no diretório atual.
Execute dentro do clone do repositório:
    git clone https://github.com/armazen-nft/QuantumCore
    cd QuantumCore
    python recreate.py
    git add -A && git commit -m "feat: scaffold QuantumCore v0.1" && git push
"""

import os
import textwrap

FILES = {}

FILES["README.md"] = textwrap.dedent("""\
# QuantumCore — OpenFM Computer (P2P)

> *Computador FM foi um método usado nos anos 1980 para transmitir programas
> de computador pelo rádio FM. QuantumCore ressuscita essa ideia com protocolos
> modernos, rede P2P e hardware comum.*

## O que é

QuantumCore transforma qualquer computador num nó de transmissão e recepção
de dados via áudio ou FM — sem internet, sem servidor central.

Cada nó pode **transmitir · receber · armazenar · retransmitir**.

```
arquivo → pacotes → compressão → FEC → FSK → áudio/FM
                                               ↓
                              armazenamento ← verificação ← demodulação
                                    ↓
                              retransmissão P2P
```

## Características

| | |
|---|---|
| Modulação | FSK (1200 / 2400 Hz) |
| Baud rate | 1200 bps |
| Payload | 256 bytes / pacote |
| Compressão | zlib |
| FEC | Reed-Solomon (reedsolo) |
| Rede | Gossip broadcast |
| Hardware mínimo | PC + placa de áudio |
| Opcional | SDR (RTL-SDR, HackRF) |

## Instalação

```bash
pip install -r requirements.txt
```

## Uso rápido

```bash
# transmitir
python examples/send_file.py arquivo.zip

# receber
python examples/receive_file.py

# rodar nó P2P completo
python examples/p2p_node.py
```

## Estrutura

```
core/        encoder, decoder, packet, fec
modem/       modulator, demodulator
audio/       audio_tx, audio_rx
network/     node, peer_discovery, retransmit
examples/    send_file, receive_file, p2p_node
docs/        protocol.md, architecture.md
```

## Modos de operação

1. **Áudio puro** — alto-falante → microfone (teste local)
2. **Cabo de áudio** — PC → rádio FM (transmissão real)
3. **SDR** — PC → SDR → antena (longo alcance)

## Licença

MIT
""")

FILES["requirements.txt"] = textwrap.dedent("""\
numpy>=1.24
scipy>=1.10
sounddevice>=0.4
reedsolo>=1.7
""")

FILES["docs/protocol.md"] = textwrap.dedent("""\
# OpenFM Protocol v0.1

## Formato do pacote

| Campo         | Tamanho | Descrição                        |
|---------------|---------|----------------------------------|
| VERSION       | 1 byte  | versão do protocolo (0x01)       |
| NODE_ID       | 4 bytes | identificador do nó origem       |
| PACKET_ID     | 2 bytes | índice do pacote                 |
| TOTAL_PACKETS | 2 bytes | total de pacotes no stream       |
| PAYLOAD_SIZE  | 2 bytes | tamanho do payload (≤ 256)       |
| CRC32         | 4 bytes | checksum do payload              |
| PAYLOAD       | ≤ 256 B | dados comprimidos + FEC          |

Total de overhead: 15 bytes por pacote.

## Modulação FSK

```
bit 0 → 1200 Hz
bit 1 → 2400 Hz
baud  → 1200 bps
sample rate → 44100 Hz
```

## FEC

Reed-Solomon (10 bytes de paridade por bloco de 246 bytes de dados).

## Fluxo de transmissão

1. Comprimir payload (zlib)
2. Dividir em chunks de 246 bytes
3. Aplicar RS(246,10) → bloco de 256 bytes
4. Montar pacote com header
5. Serializar para bits
6. Modular FSK
7. Transmitir via áudio

## Fluxo de recepção

1. Capturar áudio
2. Demodular FSK → bits
3. Desserializar pacotes
4. Verificar CRC32
5. Decodificar RS
6. Remontar payload
7. Descomprimir zlib
""")

FILES["docs/architecture.md"] = textwrap.dedent("""\
# Arquitetura QuantumCore

## Camadas

```
┌─────────────────────────────┐
│        Aplicação            │  send_file / receive_file / p2p_node
├─────────────────────────────┤
│        Rede P2P             │  node · peer_discovery · retransmit
├─────────────────────────────┤
│        Core                 │  encoder · decoder · packet · fec
├─────────────────────────────┤
│        Modem                │  modulator · demodulator
├─────────────────────────────┤
│        Áudio                │  audio_tx · audio_rx
└─────────────────────────────┘
```

## Topologia gossip

Cada nó escuta continuamente.
Ao receber dados novos, retransmite após janela aleatória (0–5 s).
Duplicatas são descartadas por (NODE_ID, PACKET_ID).

## Integração SDR (futuro)

Substituir audio_tx/audio_rx por driver SDR mantendo a mesma API:
```python
class SDRBackend:
    def transmit(self, signal): ...
    def record(self, duration): ...
```
""")

FILES["core/packet.py"] = textwrap.dedent('''\
"""Serialização e desserialização de pacotes OpenFM."""

import os
import struct
import zlib

VERSION = 0x01
NODE_ID = int.from_bytes(os.urandom(4), "big")  # gerado na inicialização
HEADER_FMT = ">BIHHHI"  # version(1) node_id(4) pkt_id(2) total(2) size(2) crc(4)
HEADER_SIZE = struct.calcsize(HEADER_FMT)  # 15 bytes


def create_packet(payload: bytes, packet_id: int, total_packets: int = 0) -> bytes:
    crc = zlib.crc32(payload) & 0xFFFFFFFF
    header = struct.pack(
        HEADER_FMT,
        VERSION,
        NODE_ID,
        packet_id,
        total_packets,
        len(payload),
        crc,
    )
    return header + payload


def parse_packet(data: bytes) -> dict | None:
    if len(data) < HEADER_SIZE:
        return None

    version, node_id, pkt_id, total, size, crc = struct.unpack(
        HEADER_FMT,
        data[:HEADER_SIZE],
    )
    payload = data[HEADER_SIZE : HEADER_SIZE + size]
    if zlib.crc32(payload) & 0xFFFFFFFF != crc:
        return None

    return {
        "version": version,
        "node_id": node_id,
        "packet_id": pkt_id,
        "total_packets": total,
        "payload": payload,
    }
''')

FILES["core/fec.py"] = textwrap.dedent('''\
"""FEC com Reed-Solomon via reedsolo."""

from reedsolo import RSCodec

_RS = RSCodec(10)  # 10 bytes de paridade


def encode(data: bytes) -> bytes:
    return bytes(_RS.encode(data))


def decode(data: bytes) -> bytes:
    decoded, _, _ = _RS.decode(data)
    return bytes(decoded)
''')

FILES["core/encoder.py"] = textwrap.dedent('''\
"""Codifica um arquivo em lista de pacotes prontos para modulação."""

import zlib

from core.fec import encode as fec_encode
from core.packet import create_packet

CHUNK = 246  # 246 dados + 10 paridade = 256 payload


def encode_file(path: str) -> list[bytes]:
    with open(path, "rb") as f:
        data = zlib.compress(f.read(), level=6)

    chunks = [data[i : i + CHUNK] for i in range(0, len(data), CHUNK)]
    total = len(chunks)
    packets = []

    for idx, chunk in enumerate(chunks):
        protected = fec_encode(chunk)
        pkt = create_packet(protected, packet_id=idx, total_packets=total)
        packets.append(pkt)

    return packets


def packet_to_bits(packet: bytes) -> list[int]:
    bits = []
    for byte in packet:
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)
    return bits
''')

FILES["core/decoder.py"] = textwrap.dedent('''\
"""Reconstrói um arquivo a partir de pacotes recebidos."""

import zlib

from core.fec import decode as fec_decode
from core.packet import parse_packet


def bits_to_bytes(bits: list[int]) -> bytes:
    out = bytearray()
    for i in range(0, len(bits) - 7, 8):
        byte = 0
        for j in range(8):
            byte = (byte << 1) | bits[i + j]
        out.append(byte)
    return bytes(out)


def decode_packets(raw_packets: list[bytes]) -> bytes | None:
    parsed = {}
    for raw in raw_packets:
        p = parse_packet(raw)
        if p:
            try:
                payload = fec_decode(p["payload"])
                parsed[p["packet_id"]] = (payload, p["total_packets"])
            except Exception:
                pass

    if not parsed:
        return None

    total = list(parsed.values())[0][1]
    if len(parsed) < total:
        return None  # pacotes faltando

    ordered = b"".join(parsed[i][0] for i in sorted(parsed))
    return zlib.decompress(ordered)
''')

FILES["modem/modulator.py"] = textwrap.dedent('''\
"""Modulação FSK: bit 0 → 1200 Hz · bit 1 → 2400 Hz."""

import numpy as np

SAMPLE_RATE = 44100
BAUD = 1200
BIT_SAMPLES = SAMPLE_RATE // BAUD  # 36 amostras por bit
F0 = 1200.0  # frequência para bit 0
F1 = 2400.0  # frequência para bit 1


def modulate(bits: list[int]) -> np.ndarray:
    t = np.linspace(0, 1 / BAUD, BIT_SAMPLES, endpoint=False)
    segments = [np.sin(2 * np.pi * (F1 if b else F0) * t) for b in bits]
    return np.concatenate(segments).astype(np.float32)
''')

FILES["modem/demodulator.py"] = textwrap.dedent('''\
"""Demodulação FSK por energia de banda."""

import numpy as np

SAMPLE_RATE = 44100
BAUD = 1200
BIT_SAMPLES = SAMPLE_RATE // BAUD
F0 = 1200.0
F1 = 2400.0

# vetores de correlação pré-calculados
_t = np.linspace(0, 1 / BAUD, BIT_SAMPLES, endpoint=False)
_C0 = np.exp(1j * 2 * np.pi * F0 * _t)
_C1 = np.exp(1j * 2 * np.pi * F1 * _t)


def demodulate(signal: np.ndarray) -> list[int]:
    bits = []
    for i in range(0, len(signal) - BIT_SAMPLES + 1, BIT_SAMPLES):
        seg = signal[i : i + BIT_SAMPLES]
        e0 = abs(np.dot(seg, _C0.conj()))
        e1 = abs(np.dot(seg, _C1.conj()))
        bits.append(1 if e1 > e0 else 0)
    return bits
''')

FILES["audio/audio_tx.py"] = textwrap.dedent('''\
"""Transmissão via saída de áudio."""

import numpy as np
import sounddevice as sd

from modem.modulator import SAMPLE_RATE

PREAMBLE_DURATION = 0.5  # segundos de tom de sincronismo


def _preamble() -> np.ndarray:
    t = np.linspace(0, PREAMBLE_DURATION, int(SAMPLE_RATE * PREAMBLE_DURATION))
    return np.sin(2 * np.pi * 1200 * t).astype(np.float32)


def transmit(signal: np.ndarray):
    full = np.concatenate([_preamble(), signal, _preamble()])
    sd.play(full, SAMPLE_RATE)
    sd.wait()
''')

FILES["audio/audio_rx.py"] = textwrap.dedent('''\
"""Captura de áudio para recepção."""

import numpy as np
import sounddevice as sd

from modem.modulator import SAMPLE_RATE


def record(duration: float) -> np.ndarray:
    audio = sd.rec(
        int(duration * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32",
    )
    sd.wait()
    return audio.flatten()
''')

FILES["network/node.py"] = textwrap.dedent('''\
"""Nó P2P: escuta, armazena e retransmite pacotes."""

import random
import time

from audio.audio_rx import record
from audio.audio_tx import transmit
from core.decoder import bits_to_bytes
from core.encoder import packet_to_bits
from core.packet import parse_packet
from modem.demodulator import demodulate
from modem.modulator import modulate

LISTEN_DURATION = 10  # segundos por ciclo de escuta
RETRANSMIT_WINDOW = 5  # jitter máximo antes de retransmitir

_seen: set[tuple] = set()
_store: list[bytes] = []


def _uid(pkt: dict) -> tuple:
    return (pkt["node_id"], pkt["packet_id"])


def run():
    print("[node] iniciando loop P2P…")
    while True:
        signal = record(LISTEN_DURATION)
        bits = demodulate(signal)
        raw = bits_to_bytes(bits)

        # divide em chunks de tamanho de pacote (heurístico)
        new_packets = []
        for i in range(0, len(raw), 271):  # 15 header + 256 payload
            pkt = parse_packet(raw[i:])
            if pkt and _uid(pkt) not in _seen:
                _seen.add(_uid(pkt))
                _store.append(raw[i : i + 271])
                new_packets.append(raw[i : i + 271])
                print(f"[node] pkt recebido: {_uid(pkt)}")

        if new_packets:
            time.sleep(random.uniform(0, RETRANSMIT_WINDOW))
            for pkt_bytes in new_packets:
                signal_out = modulate(packet_to_bits(pkt_bytes))
                transmit(signal_out)
                print(f"[node] retransmitido {len(pkt_bytes)} bytes")
''')

FILES["network/peer_discovery.py"] = textwrap.dedent('''\
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
''')

FILES["network/retransmit.py"] = textwrap.dedent('''\
"""Retransmissão de pacotes via UDP para peers descobertos."""

import socket

from network.peer_discovery import get_peers

PORT = 50701


def retransmit_udp(packets: list[bytes]):
    peers = get_peers()
    if not peers:
        return
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for peer in peers:
        for pkt in packets:
            sock.sendto(pkt, (peer, PORT))
''')

FILES["examples/send_file.py"] = textwrap.dedent('''\
"""Transmite um arquivo via FSK/áudio."""

import sys

from audio.audio_tx import transmit
from core.encoder import encode_file, packet_to_bits
from modem.modulator import modulate


def main():
    if len(sys.argv) < 2:
        print("uso: python send_file.py <arquivo>")
        sys.exit(1)

    path = sys.argv[1]
    packets = encode_file(path)
    print(f"[tx] {len(packets)} pacotes gerados")

    for i, pkt in enumerate(packets):
        bits = packet_to_bits(pkt)
        signal = modulate(bits)
        print(f"[tx] transmitindo pacote {i + 1}/{len(packets)} …")
        transmit(signal)

    print("[tx] concluído")


if __name__ == "__main__":
    main()
''')

FILES["examples/receive_file.py"] = textwrap.dedent('''\
"""Recebe pacotes via áudio e reconstrói o arquivo."""

import sys

from audio.audio_rx import record
from core.decoder import bits_to_bytes, decode_packets
from core.packet import parse_packet
from modem.demodulator import demodulate

DURATION = 60  # segundos de escuta
OUTPUT_PATH = "received_output.bin"


def main():
    print(f"[rx] escutando por {DURATION}s …")
    signal = record(DURATION)
    bits = demodulate(signal)
    raw = bits_to_bytes(bits)

    # coleta todos os pacotes válidos do stream
    raw_packets = []
    pkt_size = 271
    for i in range(0, len(raw) - pkt_size + 1, pkt_size):
        chunk = raw[i : i + pkt_size]
        if parse_packet(chunk):
            raw_packets.append(chunk)

    print(f"[rx] {len(raw_packets)} pacotes válidos")
    data = decode_packets(raw_packets)

    if data is None:
        print("[rx] falha na reconstrução (pacotes insuficientes)")
        sys.exit(1)

    with open(OUTPUT_PATH, "wb") as f:
        f.write(data)
    print(f"[rx] arquivo salvo em {OUTPUT_PATH} ({len(data)} bytes)")


if __name__ == "__main__":
    main()
''')

FILES["examples/p2p_node.py"] = textwrap.dedent('''\
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
''')

for pkg in ("core", "modem", "audio", "network", "examples"):
    FILES[f"{pkg}/__init__.py"] = ""


def main():
    root = os.path.dirname(os.path.abspath(__file__))
    for rel, content in FILES.items():
        path = os.path.join(root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  ✓  {rel}")

    print(
        f"\n{len(FILES)} arquivos criados. Agora:\n"
        "  git add -A\n"
        '  git commit -m "feat: scaffold QuantumCore v0.1"\n'
        "  git push"
    )


if __name__ == "__main__":
    main()
