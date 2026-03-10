"""iOS audio backend placeholder.

Expected implementation: AudioUnit bridge through pyobjus/rubicon.
"""


class IOSAudioIO:
    def record(self, duration: float, sample_rate: int = 48_000):
        raise NotImplementedError("iOS backend requires a pyobjus bridge")

    def playback(self, samples, sample_rate: int = 48_000) -> None:
        raise NotImplementedError("iOS backend requires a pyobjus bridge")
