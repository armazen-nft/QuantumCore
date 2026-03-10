from modem.modulator import PREAMBLE, SAMPLES_PER_BIT


def _bits_to_bytes(bits):
    bits = bits[: (len(bits) // 8) * 8]
    out = bytearray()
    for i in range(0, len(bits), 8):
        b = 0
        for bit in bits[i : i + 8]:
            b = (b << 1) | int(bit)
        out.append(b)
    return bytes(out)


def demodulate(audio):
    """Demodula sinal gerado por modem.modulator.modulate."""
    n = len(audio) // SAMPLES_PER_BIT
    if n == 0:
        return []

    bits = []
    for i in range(n):
        chunk = audio[i * SAMPLES_PER_BIT : (i + 1) * SAMPLES_PER_BIT]
        mean = sum(chunk) / len(chunk)
        bits.append(1 if mean > 0 else 0)

    data = _bits_to_bytes(bits)
    idx = data.find(PREAMBLE)
    if idx < 0:
        return []

    rest = data[idx + len(PREAMBLE) :]
    if len(rest) < 4:
        return []

    size = int.from_bytes(rest[:4], "big")
    packet = rest[4 : 4 + size]
    if len(packet) != size:
        return []

    return [packet]
