import unittest
from prime_number.erastothenes import erastothenes

class TestErastothenes(unittest.TestCase):
    def test_correct(self):
        scale=10
        result=erastothenes(scale)
        print(result)
        assert result == [2,3,5,7]
    

