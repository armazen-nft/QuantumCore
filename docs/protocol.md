# Protocol (draft)

## Packet format

QuantumCore uses a fixed packet size of **258 bytes**:

- Header: 6 bytes
  - Magic: `QC` (2 bytes)
  - Sequence number: uint16 big-endian (2 bytes)
  - Payload length: uint16 big-endian (2 bytes)
- Payload: 248 bytes (zero padded)
- CRC32: 4 bytes (big-endian) over header+payload

## Modulation (current)

- FSK, 1200 baud
- Sample rate: 48 kHz
- Bit mapping:
  - `1` => 1200 Hz
  - `0` => 2400 Hz
- Preamble: 32 alternating bits (`1010...`) before packet bits.

Bits are transmitted LSB-first for each byte.
