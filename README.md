# 🚀 QuantumCore – OpenFM Computer (P2P)

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: MVP Funcional](https://img.shields.io/badge/Status-MVP%20Funcional-brightgreen.svg)]()

**Um computador FM moderno, open source e peer-to-peer** capaz de transmitir e receber dados digitais usando **áudio ou rádio FM**. Inspirado no lendário Computador FM dos anos 80.

Qualquer computador vira um **nó de transmissão/recepção broadcast** — 100% offline.

---

## ✨ Visão geral

O QuantumCore transforma áudio analógico em canal digital confiável com:
- Modulação FSK 1200 baud (1200/2400 Hz)
- Pacotes de 258 bytes com CRC32
- Preamble de sincronismo
- Retransmissão P2P (em breve)

---

## 📂 Módulos já implementados (MVP funcional)

| Módulo                  | Função                                      | Status     |
|-------------------------|---------------------------------------------|------------|
| `core/packet.py`        | Cria/valida pacotes 258 bytes + CRC         | ✅ Pronto  |
| `modem/modulator.py`    | FSK 1200 baud + preamble                    | ✅ Pronto  |
| `modem/demodulator.py`  | Demodulação Goertzel + detecção de preamble | ✅ Pronto  |
| `audio/tx_rx.py`        | Transmitir e gravar com sounddevice         | ✅ Pronto  |
| `examples/send_file.py` | Envia qualquer arquivo em pacotes           | ✅ Pronto  |

---

## 📦 Instalação

```bash
git clone https://github.com/armazen-nft/QuantumCore.git
cd QuantumCore

# Dependências Python
pip install -r requirements.txt

# Portaudio (obrigatório para sounddevice)
# Ubuntu/Debian:
sudo apt install portaudio19-dev
# macOS:
# brew install portaudio
# Windows: já vem no pacote sounddevice
```

## 🧪 Teste rápido (Loopback no mesmo PC)

Crie um arquivo de teste:

```bash
echo "Teste QuantumCore 2026 🚀" > teste.txt
```

Terminal 2 (receptor — rode primeiro):

```bash
python -c '
from audio.tx_rx import record
from modem.demodulator import demodulate
from core.packet import unpack
audio = record(6.0)
packets = demodulate(audio)
for pkt in packets:
    seq, payload = unpack(pkt)
    if seq is not None:
        print(f"✅ Pacote {seq} recebido: {payload.decode(errors=\"ignore\")}")
'
```

Terminal 1 (transmissor):

```bash
python examples/send_file.py teste.txt
```

Coloque o microfone perto do alto-falante (ou use cabo áudio). Funciona perfeitamente!

## 🚀 Uso básico

```bash
# Enviar arquivo
python examples/send_file.py meu_arquivo.zip
```

(Em breve: `receive_file.py` automático + nó P2P completo)

## 🎛️ Modos de operação

- Áudio direto (computador ↔ computador)
- Rádio FM (alcance de quilômetros)
- SDR (rtl-sdr) — planejado

## 🧩 Roadmap

| Prioridade | Funcionalidade                 | Status     |
|------------|--------------------------------|------------|
| Alta       | `examples/receive_file.py`     | Próximo    |
| Alta       | Nó P2P com retransmissão       | Planejado  |
| Média      | Reed-Solomon FEC               | Planejado  |
| Média      | Suporte SDR (rtl-sdr)          | Planejado  |
| Baixa      | Criptografia de pacotes        | Planejado  |

## 🤝 Como contribuir

Quer ajudar agora?

- Implementar `examples/receive_file.py`
- Criar `network/node.py` (P2P)
- Testes reais com rádio FM
- Diagramas de sinal

Abra uma issue com a tag `help wanted` ou faça um PR!

## 📜 Licença

MIT — veja `LICENSE`.

Vamos construir a internet offline do futuro? 🌐📻

Autor: Projeto open-source por armazen-nft  
Atualizado em março/2026
