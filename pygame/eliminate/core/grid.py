import random
from enum import Enum

from core.main_config import MainConfig
from domain.monster import Monster
from domain.stone import Stone


class CellType(Enum):
    STONE = 0
    MONSTER = 1


STONE_DEFAULT_HP = 1


class Grid:
    def __init__(self):
        self.configs = MainConfig()
        self.current_grid = 0
        self.grid = []
        self.type_count = {}

        for monster in self.configs.monsters:
            self.type_count[monster['id']] = 0

    def generate_grid(self, grid_id=0):
        self.current_grid = grid_id
        data = self.configs.grids[grid_id]['data']
        for index in range(len(data)):
            type_ = data[index]

            if type_ == CellType.MONSTER.value:
                self.grid.append(Monster(index, self.random_monster_ref(), 1))
            if type_ == CellType.STONE.value:
                # TODO generate stone hp
                self.grid.append(Stone(index, STONE_DEFAULT_HP))

    # TODO The result satisfies the average distribution.
    def random_monster_ref(self) -> str:
        monster_dict = random.choice(self.configs.monsters)
        ref_id = monster_dict['id']
        self.type_count[ref_id] += 1
        return ref_id

    def show(self):
        grid_ = self.configs.grids[self.current_grid]

        for i in range(grid_['row']):
            for j in range(grid_['col']):
                print("%6s" % (self.grid[i * j + j].show()), end='')
            print()
        print()



