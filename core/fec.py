"""FEC com Reed-Solomon via reedsolo."""

from reedsolo import RSCodec

_RS = RSCodec(10)  # 10 bytes de paridade


def encode(data: bytes) -> bytes:
    return bytes(_RS.encode(data))


def decode(data: bytes) -> bytes:
    decoded, _, _ = _RS.decode(data)
    return bytes(decoded)
