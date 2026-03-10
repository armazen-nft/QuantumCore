"""Android audio backend placeholder.

Expected implementation: OpenSL ES / AudioTrack bridge through pyjnius/Kivy/BeeWare.
"""


class AndroidAudioIO:
    def record(self, duration: float, sample_rate: int = 48_000):
        raise NotImplementedError("Android backend requires a pyjnius/Kivy bridge")

    def playback(self, samples, sample_rate: int = 48_000) -> None:
        raise NotImplementedError("Android backend requires a pyjnius/Kivy bridge")
