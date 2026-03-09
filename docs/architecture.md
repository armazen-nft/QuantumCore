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
