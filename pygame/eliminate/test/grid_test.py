import unittest

from core.grid import Grid


class TestGrid(unittest.TestCase):
    def test_generate(self):
        grid = Grid()
        grid.init_generate_grid()

        self.assertEqual(len(grid.grid), 16)

        for cell in grid.grid:
            print(str(cell))

        print(grid.type_count)

        grid.show()

    def test_show(self):
        grid = Grid()
        grid.init_generate_grid()
        grid.show()

        print('数量统计', grid.type_count)

    def test_check(self):
        grid = Grid(1)
        grid.init_generate_grid()

        grid.show()
        print('数量统计', grid.type_count)

        grid.check_eliminate()

        for state in grid.direct_states:
            print(state, grid.direct_states[state])

    def test_generate_complete(self):
        grid = Grid(3)
        grid.init_generate_grid()

        # self.assertEqual(len(grid.grid), 36)
        grid.simple_show()

        grid.check_eliminate()
        for state in grid.direct_states:
            print(state, grid.direct_states[state])

    def test_probably(self):
        grid = Grid(3)
        grid.init_generate_grid()

        grid.simple_show()
        grid.check_eliminate()
        for state in grid.probably_eliminate:
            print(state, grid.probably_eliminate[state])


if __name__ == '__main__':
    unittest.main()
