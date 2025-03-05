import unittest

from ctime.clock import (
    clock_monotonic,
    clock_monotonic_coarse,
    clock_monotonic_raw,
    clock_realtime,
    clock_realtime_coarse,
)


class TestCTime(unittest.TestCase):
    def test_clock_monotonic_raw(self):
        # Test that the function returns a non-negative integer
        result = clock_monotonic_raw()
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, 0)

    def test_clock_monotonic(self):
        # Test that the function returns a non-negative integer
        result = clock_monotonic()
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, 0)

    def test_clock_realtime(self):
        # Test that the function returns a non-negative integer
        result = clock_realtime()
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, 0)

    def test_clock_monotonic_coarse(self):
        # Test that the function returns a non-negative integer
        result = clock_monotonic_coarse()
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, 0)

    def test_clock_realtime_coarse(self):
        # Test that the function returns a non-negative integer
        result = clock_realtime_coarse()
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, 0)

    def test_monotonic_increases(self):
        # Test that monotonic clocks increase over time
        first = clock_monotonic_raw()
        second = clock_monotonic_raw()
        self.assertGreaterEqual(second, first)

        first = clock_monotonic()
        second = clock_monotonic()
        self.assertGreaterEqual(second, first)

        first = clock_monotonic_coarse()
        second = clock_monotonic_coarse()
        self.assertGreaterEqual(second, first)


if __name__ == "__main__":
    unittest.main()
