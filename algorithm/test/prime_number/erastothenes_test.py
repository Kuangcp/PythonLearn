import unittest
from prime_number.erastothenes import eratosthenes


class TestEratosthenes(unittest.TestCase):
    def test_correct(self):
        scale = 10
        result = eratosthenes(scale)
        print(result)
        assert result == [2, 3, 5, 7]
