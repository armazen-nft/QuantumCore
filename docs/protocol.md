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
