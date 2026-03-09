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
