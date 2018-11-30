import unittest


class Tool(unittest.TestCase):

    def test_generate_data(self):
        for i in range(100):
            print('1,', end='')


if __name__ == '__main__':
    unittest.main()
