import unittest

import sort.sort_box as box


def generate_data():
    return [1, 2, 3, 45, 6, 7]


def check_sorted(data) -> bool:
    for i in range(0, len(data) - 1):
        if data[i] > data[i + 1]:
            return False
    return True


class TestSort(unittest.TestCase):

    def test_box_sort(self):
        result = box.box(generate_data())
        print(result)


if __name__ == '__main__':
    unittest.main()
