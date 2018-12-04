import random

from core.main_config import MainConfig
from domain.cell_state import CellState
from domain.direct_type import DirectType
from domain.enum_type import OrderType, CellType
from domain.monster import Monster
from domain.stone import Stone
from util.log import logging


class CellVO:
    def __init__(self, ref_id, order, index, count):
        self.index = index
        self.ref_id = ref_id  # 期望替换过来的ref_id
        self.order = order  # 期望的order
        self.count = count  # 重叠的权重

    def __repr__(self) -> str:
        return 'ref_id=' + self.ref_id + ' index=' + str(self.index) + ' count=' + str(self.count)


class Grid:
    def __init__(self, grid_id=0):
        self.configs = MainConfig()
        self.current_grid = self.configs.grids[grid_id]
        self.row = self.current_grid['row']
        self.col = self.current_grid['col']
        # TODO use dict, more quickly?
        self.grid = []  # Monster or  Stone Object
        self.type_count = {}

        self.direct_states = {}  # able to eliminate (length more than 2)
        self.probably_eliminate = {}  # probably to eliminate (length equal to 2)

        # init monster count
        for monster in self.configs.monsters:
            self.type_count[monster['id']] = 0

    def init_generate_grid(self):
        data = self.current_grid['data']
        for index in range(len(data)):
            type_ = data[index]

            if type_ == CellType.MONSTER.value:
                self.grid.append(self.create_monster(index))
            if type_ == CellType.STONE.value:
                # TODO generate stone hp
                self.grid.append(self.create_stone(index))

        while True:
            self.check_eliminate()
            for direct in self.direct_states:
                states = self.direct_states[direct]
                for state in states:
                    indexes = state.indexes
                    index = random.choice(indexes)

                    monster = self.grid[index]
                    monster.ref_id = self.replace_monster_with_other(monster.ref_id)
            self.check_eliminate()
            if len(self.direct_states) == 0:
                break

    @staticmethod
    def create_stone(index):
        return Stone(index, Stone.random_hp())

    def create_monster(self, index):
        return Monster(index, self.random_monster_ref(), OrderType.D, 1)

    def replace_monster_with_other(self, ref_id) -> str:
        self.type_count[ref_id] -= 1
        ids = []
        for monster in self.configs.monsters:
            if monster['id'] != ref_id:
                ids.append(monster['id'])
        other_id = random.choice(ids)
        return other_id

    # TODO The monster satisfies the average distribution.
    def random_monster_ref(self) -> str:
        # return 'X'
        monster_dict = random.choice(self.configs.monsters)
        ref_id = monster_dict['id']
        self.type_count[ref_id] += 1
        return ref_id

    def check_eliminate(self):
        self.direct_states = {}
        self.probably_eliminate = {}

        self.check_east()
        self.check_south()
        self.check_north_east()
        self.check_south_east()

    def check_east(self):
        for x in range(self.row):
            temp = []
            for y in range(0, self.col):
                cell = self.grid[self.col * x + y]
                temp = self.compare_monster(cell, temp, DirectType.EAST)
            self.add_monster(temp, DirectType.EAST)

    def check_south(self):
        for y in range(self.col):
            temp = []
            for x in range(self.row):
                cell = self.grid[self.col * x + y]
                temp = self.compare_monster(cell, temp, DirectType.SOUTH)
            self.add_monster(temp, DirectType.SOUTH)

    def check_south_east(self):
        for i in range(self.col - 2):
            temp = []
            for j in range(i, (self.row - i) * self.col, self.col + 1):
                cell = self.grid[j]
                temp = self.compare_monster(cell, temp, DirectType.SOUTH_EAST)
            self.add_monster(temp, DirectType.SOUTH_EAST)

        for i in range(self.col, self.col * (self.row - 1), self.col):
            temp = []
            for j in range(i, self.col * self.row, self.col + 1):
                cell = self.grid[j]
                temp = self.compare_monster(cell, temp, DirectType.SOUTH_EAST)
            self.add_monster(temp, DirectType.SOUTH_EAST)

    def check_north_east(self):
        for i in range(1, self.col):
            temp = []
            for j in range(i, i * self.col + 1, self.col - 1):
                cell = self.grid[j]
                temp = self.compare_monster(cell, temp, DirectType.NORTH_EAST)
            self.add_monster(temp, DirectType.NORTH_EAST)

        if self.row < 3:
            return
        for i in range(self.col * 2 - 1, (self.row - 1) * self.col - 1, self.col):
            temp = []
            for j in range(i, self.row * self.col - 1, self.col - 1):
                cell = self.grid[j]
                temp = self.compare_monster(cell, temp, DirectType.NORTH_EAST)
            self.add_monster(temp, DirectType.NORTH_EAST)

    def compare_monster(self, cell, temp, direct_type):
        if len(temp) == 0:
            if cell.get_type() == CellType.MONSTER:
                return [cell]
            return []

        temp_ = temp[0]
        # logging.debug(str(cell) + ' <--> ' + str(temp_))

        if temp_.get_type() == cell.get_type() == CellType.MONSTER and temp_.is_same(cell):
            temp.append(cell)
        elif cell.get_type() == CellType.MONSTER:
            self.add_monster(temp, direct_type)
            temp = [cell]
        else:
            temp = []
        return temp

    def add_monster(self, temp, direct_type):
        if len(temp) == 0:
            return

        temp = sorted(temp, key=lambda a: a.order.value)

        indexes = []
        result = []
        state = None
        for i in range(len(temp)):
            indexes.append(temp[i].index)
            if i == 0:
                state = CellState(temp[i].ref_id, indexes, temp[i].order, direct_type)
                result.append(state)

            elif temp[i].order != temp[i - 1].order:
                state = CellState(temp[i].ref_id, indexes, temp[i].order, direct_type)
                result.append(state)
                indexes = []
            else:
                state.indexes = indexes

        if len(temp) <= 2:
            if direct_type not in self.probably_eliminate:
                self.probably_eliminate[direct_type] = [state]
            else:
                self.probably_eliminate[direct_type].append(state)
        else:
            if direct_type not in self.direct_states:
                self.direct_states[direct_type] = [state]
            else:
                self.direct_states[direct_type].append(state)

    # 生成/掉落
    def generate_new(self):
        pass

    # 交换和消除
    def transfer_and_eliminate(self):
        pass

    # 记录上场
    def record_monster(self):
        pass

    def best_plan_to_transfer(self) -> (CellVO, CellVO):
        """
        找出最佳方案
        :return: (CellVO, CellVO) 需要交换的两个 cell
        """
        cells = self.get_alternative_monster()
        if len(cells) == 0:
            logging.info("can't find any transfer")
            return ()

        if len(cells) > 1:
            first_cell = None
            out_ref_id = None

            for cell in cells:
                # TODO can group by count, then compare all in order
                logging.debug('expect in:%s actual out:%s %s' % (cell.ref_id, self.grid[cell.index].ref_id, cell.count))

                if first_cell is None:
                    first_cell = cell
                    out_ref_id = self.grid[cell.index].ref_id
                    continue

                if out_ref_id == cell.ref_id and not self.is_intersect(first_cell, cell):
                    # TODO 两个期望互不相交
                    return first_cell, cell

        # TODO get one
        first = cells[0]
        cell = self.get_completion_one(first)
        if cell is not None:
            return first, cell

        return ()

    def is_intersect(self, a, b) -> bool:
        cell_a = self.get_nearby_index_lists(a)
        cell_b = self.get_nearby_index_lists(b)
        temp = []
        for indexes in cell_a:
            temp.extend(indexes)

        for indexes in cell_b:
            for index in indexes:
                if index in temp:
                    return True
        return False

    # 根据 index 和 期望的ref_id 找出附近 最大的关联结构 [[index],[index]]
    def get_nearby_index_lists(self, target) -> [[], []]:
        current = target.index
        result = []

        for direct in self.probably_eliminate:
            state_list = self.probably_eliminate[direct]
            for cell in state_list:
                pre = cell.get_pre(self)
                next_ = cell.get_next(self)
                if pre == current or next_ == current:
                    result.append(cell.indexes)

        return result

    def get_completion_one(self, cell):
        """
        first find in outside , then find min count inside
        :param cell:
        """
        index_lists = self.get_nearby_index_lists(cell)
        temp = []
        for indexes in index_lists:
            temp.extend(index_lists)
        for cell in self.grid:
            print(cell)

        return None

    # 获取备选方案 按权重倒序排序
    def get_alternative_monster(self) -> [CellVO]:
        self.check_eliminate()

        result = []
        result.extend(self.cell_vo_by_successive())
        # result.extend(self.cell_vo_by_discontinuous())
        if len(result) != 0:
            result = sorted(result, key=lambda cell_vo: cell_vo.count, reverse=True)
        return result

    # 分为 xo ox xx
    def cell_vo_by_successive(self) -> [CellVO]:
        vo_dict = {}  # id -> [(order,index)]
        for direct in self.probably_eliminate:
            state_list = self.probably_eliminate[direct]
            for cell in state_list:
                pre = cell.get_pre(self)
                next_ = cell.get_next(self)
                # logging.debug('%s %s - %s' % (cell, pre, next_))

                if cell.ref_id not in vo_dict:
                    vo_dict[cell.ref_id] = []

                id_ = vo_dict[cell.ref_id]
                if pre is not None:
                    id_.append((cell.order, pre))
                if next_ is not None:
                    id_.append((cell.order, next_))

        result = []
        for ref_id in vo_dict:
            vo_tuple = vo_dict[ref_id]
            # logging.debug('%s: %s' % (ref_id, str(vo_tuple)))

            result.extend(self.get_repeated_indexes(ref_id, vo_tuple))
        return result

    # # TODO xxox oxx, oxx xox
    # def cell_vo_by_discontinuous(self) -> [CellVO]:
    #
    #     return []

    def get_repeated_indexes(self, ref_id, vo_tuple) -> [CellVO]:
        temp = {}  # ref_id_order->count
        result = []
        for order, index in vo_tuple:
            base = 1
            if index < 0:
                index *= -1
                base = 1 / 8

            if index not in temp:
                temp[(order, index)] = base
            else:
                temp[(order, index)] = temp[(order, index)] + base

        for order, index in temp:
            if temp[(order, index)] > 0.75 and self.grid[index].get_type() == CellType.MONSTER:
                cell = CellVO(ref_id, order, index, temp[(order, index)])
                result.append(cell)
        return result

    def show(self):
        for i in range(self.row):
            for j in range(self.col):
                print("%8s" % (self.grid[i * self.col + j].show()), end='')
            print()
        print()

    def simple_show(self):
        for i in range(self.row):
            for j in range(self.col):
                print("%2s" % (self.grid[i * self.col + j].simple_show()), end='')
            print()
        print()
