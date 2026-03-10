# QuantumCore

QuantumCore é um protótipo de comunicação digital por áudio/FM com arquitetura modular.

## Novidades implementadas

- Bridge de áudio multiplataforma em `audio/audio_bridge.py` com `AudioIO` e backends `SoundDeviceAudioIO`, `AndroidAudioIO` e `IOSAudioIO`.
- Integração da bridge nos módulos `audio/audio_tx.py` e `audio/audio_rx.py`.
- Novo módulo SDR em `sdr/`:
  - `sdr/sdr_common.py` para conversão real→IQ e reamostragem.
  - `sdr/sdr_tx.py` para transmissão TX via SoapySDR.
- CLI de envio em `examples/send_file.py` com modo `--mode audio|sdr`, `--freq` e `--backend`.
- Web monitor em `web_monitor/` com API `/api/peers` e interface HTML em `web_monitor/templates/index.html`.
- Exemplo de nó em `examples/p2p_node.py` com `--web-monitor`.
- Testes em `tests/` cobrindo bridge de áudio, SDR TX e API do web monitor.
- Workflow CI em `.github/workflows/test.yml`.

## Estrutura

```text
QuantumCore/
├── audio/
├── sdr/
├── network/
├── web_monitor/
├── examples/
├── tests/
└── .github/workflows/
```

## Instalação

```bash
pip install -r requirements.txt
```

## Uso

### Envio por áudio

```bash
python examples/send_file.py arquivo.bin --mode audio --backend sounddevice
```

### Envio por SDR

```bash
python examples/send_file.py arquivo.bin --mode sdr --freq 98.5 --sdr-sample-rate 1000000
```

### Nó com monitor web

```bash
python examples/p2p_node.py --web-monitor --port 5000
```

Depois abra `http://localhost:5000`.
