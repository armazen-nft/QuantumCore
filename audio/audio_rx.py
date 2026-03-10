from audio.audio_tx import _LAST_TX


def record(duration: float = 1.0, device: int | None = None):
    """Recepção mock para ambiente sem hardware de áudio."""
    del duration, device
    if _LAST_TX is None:
        return []
    return list(_LAST_TX)
