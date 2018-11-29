import unittest

from core.grid import Grid


class TestGrid(unittest.TestCase):
    def test_generate(self):
        grid = Grid()
        grid.generate_grid(0)

        self.assertEqual(len(grid.grid), 16)

        for cell in grid.grid:
            print(str(cell))

        print(grid.type_count)

    def test_show(self):
        grid = Grid()
        grid.generate_grid()
        grid.show()

        print('数量统计', grid.type_count)


if __name__ == '__main__':
    unittest.main()
