import unittest
import concurrent.futures


def gcd(pair):
    a, b = pair
    low = min(a, b)
    for i in range(low, 0, -1):
        if a % i == 0 and b % i == 0:
            return i


numbers = [
    (1963309, 2265973), (1879675, 2493670), (2030677, 3814172),
    (1551645, 2229620), (1988912, 4736670), (2198964, 7876293)
]


class TestFutures(unittest.TestCase):
    def test_simple_sum(self):
        for num in numbers:
            gcd(num)

    def test_futures_sum(self):
        with concurrent.futures.ProcessPoolExecutor() as executor:
            executor.map(gcd, numbers)


if __name__ == '__main__':
    unittest.main()
