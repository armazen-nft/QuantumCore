import numpy as np

SAMPLE_RATE = 48000
BAUD_RATE = 1200
SAMPLES_PER_BIT = SAMPLE_RATE // BAUD_RATE
MARK_FREQ = 1200.0
SPACE_FREQ = 2400.0


def goertzel(samples: np.ndarray, freq: float) -> float:
    """Goertzel para detectar energia exata em 1200 Hz ou 2400 Hz"""
    N = len(samples)
    if N == 0:
        return 0.0
    k = int(0.5 + (N * freq) / SAMPLE_RATE)
    w = 2 * np.pi * k / N
    cosine = np.cos(w)
    coeff = 2 * cosine
    s1 = s2 = 0.0
    for sample in samples:
        s0 = sample + coeff * s1 - s2
        s2 = s1
        s1 = s0
    magnitude = s1 * s1 + s2 * s2 - coeff * s1 * s2
    return magnitude


def demodulate_bits(audio: np.ndarray) -> list[int]:
    """Converte áudio em sequência de bits"""
    if len(audio) < SAMPLES_PER_BIT:
        return []
    bits = []
    idx = 0
    while idx + SAMPLES_PER_BIT <= len(audio):
        window = audio[idx : idx + SAMPLES_PER_BIT]
        energy_mark = goertzel(window, MARK_FREQ)
        energy_space = goertzel(window, SPACE_FREQ)
        bit = 1 if energy_mark > energy_space else 0
        bits.append(bit)
        idx += SAMPLES_PER_BIT
    return bits


def find_preamble(bits: list[int], preamble_len: int = 32) -> int:
    """Localiza o preamble 1010... (32 bits)"""
    preamble = [1, 0] * (preamble_len // 2)
    for i in range(len(bits) - preamble_len + 1):
        if bits[i : i + preamble_len] == preamble:
            return i
    return -1


def bits_to_bytes(bits: list[int]) -> bytes:
    """Converte bits → bytes (LSB first, compatível com modulator)"""
    byte_array = []
    for i in range(0, len(bits), 8):
        byte_bits = bits[i : i + 8]
        if len(byte_bits) < 8:
            break
        byte = 0
        for j, bit in enumerate(byte_bits):
            byte |= bit << j
        byte_array.append(byte)
    return bytes(byte_array)


def demodulate(audio: np.ndarray) -> list[bytes]:
    """Demodula áudio e retorna lista de pacotes crus (258 bytes cada)"""
    bits = demodulate_bits(audio)
    preamble_start = find_preamble(bits)
    if preamble_start == -1:
        return []

    packet_bits = bits[preamble_start + 32 :]
    packet_size_bits = 258 * 8
    packets = []
    i = 0
    while i + packet_size_bits <= len(packet_bits):
        pkt_bits = packet_bits[i : i + packet_size_bits]
        pkt_bytes = bits_to_bytes(pkt_bits)
        if len(pkt_bytes) == 258:
            packets.append(pkt_bytes)
        i += packet_size_bits
    return packets
