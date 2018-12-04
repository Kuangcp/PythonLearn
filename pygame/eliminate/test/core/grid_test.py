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
        grid = Grid(2)
        grid.init_generate_grid()

        grid.simple_show()

        grid.check_eliminate()
        for state in grid.probably_eliminate:
            state_list = grid.probably_eliminate[state]
            for cell in state_list:
                print(cell.direct_type, cell.ref_id, cell.get_pre(grid), cell.indexes, cell.get_next(grid))

    def test_get_alternative_monster(self):
        grid = Grid()
        grid.init_generate_grid()

        grid.simple_show()
        # grid.show()

        result = grid.get_alternative_monster()
        for vo in result:
            print(vo)

        if len(result) == 0:
            print('There is no way to eliminate it.')

    def test_best_plan(self):
        grid = Grid()
        grid.init_generate_grid()

        grid.simple_show()
        result = grid.best_plan_to_transfer()
        for i in result:
            print('transfer ', i)


if __name__ == '__main__':
    unittest.main()
