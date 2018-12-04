import unittest

# 隐式返回None
def add(a, b) -> int:
    if a > 0:
        return a + b


# just temporary code
class Tool(unittest.TestCase):

    def test_generate_data(self):
        for i in range(100):
            print('1,', end='')

    def test_a(self):
        result = [1]
        a = [1, 4, 5]
        result.extend(a)
        print(result)

    def test_no_return(self):
        result = add(-3, 4)
        print(result)


if __name__ == '__main__':
    unittest.main()
