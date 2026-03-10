SAMPLES_PER_BIT = 16
PREAMBLE = bytes([0xAA, 0x55, 0xAA, 0x55])


def _bytes_to_bits(data: bytes):
    for b in data:
        for i in range(7, -1, -1):
            yield (b >> i) & 1


def modulate(packet: bytes):
    """Modulação digital simples NRZ bipolar para testes de loopback."""
    framed = PREAMBLE + len(packet).to_bytes(4, "big") + packet
    audio = []
    for bit in _bytes_to_bits(framed):
        symbol = 1.0 if bit else -1.0
        audio.extend([symbol] * SAMPLES_PER_BIT)
    return audio
