_LAST_TX = None


def transmit(audio, device: int | None = None) -> None:
    """Transmissão mock para ambiente sem hardware de áudio."""
    del device
    global _LAST_TX
    _LAST_TX = list(audio)
