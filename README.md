# QuantumCore
# OpenFM Computer (P2P)

Um **Computador FM moderno, open source e peer-to-peer**, capaz de transmitir e receber dados digitais usando **áudio ou rádio FM**, inspirado no histórico sistema de distribuição de software via rádio dos anos 1980.

## Novidades implementadas

- Bridge de áudio multiplataforma com abstração `AudioIO` e seleção de backend por SO ou parâmetro `--backend`.
- Integração de transmissão SDR na CLI via `--mode tx --sdr --freq`.
- Web monitor de peers com endpoint `/api/peers` e página HTML com atualização periódica.
- Testes unitários de SDR TX e workflow de CI no GitHub Actions.

## Estrutura do repositório

```
.
├── audio/
│   ├── audio_bridge.py
│   ├── audio_tx.py
│   ├── audio_rx.py
│   └── backends/
│       ├── sounddevice_backend.py
│       ├── android_backend.py
│       └── ios_backend.py
├── modem/
│   └── modulator.py
├── network/
│   ├── node.py
│   └── peer_discovery.py
├── sdr/
│   └── sdr_tx.py
├── web_monitor/
│   ├── app.py
│   └── static/index.html
├── tests/
│   └── test_sdr_tx.py
├── examples/
│   ├── send_file.py
│   ├── receive_file.py
│   └── p2p_node.py
├── .github/workflows/test.yml
├── cli.py
└── requirements.txt
```

## CLI

Transmissão por áudio:

```bash
python cli.py --mode tx --input arquivo.zip
```

Transmissão por SDR:

```bash
python cli.py --mode tx --sdr --freq 98.5 --input arquivo.zip
```

Recepção por áudio:

```bash
python cli.py --mode rx --duration 5 --backend linux
```

## Web monitor

```bash
python examples/p2p_node.py --web-monitor --port 8080
```

Acesse `http://localhost:8080` para visualizar peers ativos.

## Testes

```bash
python -m unittest discover -s tests -v
```
