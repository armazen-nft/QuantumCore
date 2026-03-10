import unittest
from unittest.mock import Mock

import numpy as np

from modem.modulator import modulate_fsk
from sdr.sdr_tx import transmit_sdr


class TestSDRTransmit(unittest.TestCase):
    def test_transmit_called_with_correct_samples(self):
        samples = modulate_fsk(b"teste", baud_rate=1200, sample_rate=48_000)
        self.assertIsInstance(samples, np.ndarray)
        self.assertEqual(samples.dtype, np.float32)

        backend = Mock()
        transmit_sdr(samples, frequency=98.5e6, backend=backend)

        backend.send.assert_called_once()
        sent_iq = backend.send.call_args.kwargs["iq_samples"]
        self.assertEqual(sent_iq.dtype, np.complex64)

    def test_frequency_parameter_passed(self):
        backend = Mock()
        samples = np.array([0.0, 0.5, -0.5], dtype=np.float32)

        transmit_sdr(samples, frequency=915e6, sample_rate=96_000, backend=backend)

        self.assertEqual(backend.send.call_args.kwargs["frequency"], 915e6)
        self.assertEqual(backend.send.call_args.kwargs["sample_rate"], 96_000)

    def test_invalid_frequency_raises_error(self):
        samples = np.array([0.0, 0.5, -0.5], dtype=np.float32)
        with self.assertRaises(ValueError):
            transmit_sdr(samples, frequency=10)


if __name__ == "__main__":
    unittest.main()
