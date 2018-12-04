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

        # direct ->[CellState]
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

    def main_loop(self, loop):
        for i in range(loop):
            self.init_generate_grid()
            self.simple_show()
            cells = self.best_plan_to_swap()
            if len(cells) == 0:
                return
            self.swap_and_eliminate(cells)

    # 生成/掉落
    def generate_new(self):
        pass

    # 记录上场
    def record_monster(self):
        pass

    # 交换和消除
    def swap_and_eliminate(self, cell_vo_tuple):
        if len(cell_vo_tuple) != 2:
            return
        self.swap_monster(cell_vo_tuple[0].index, cell_vo_tuple[1].index)
        self.synthesize_monster()

    def synthesize_monster(self):
        self.check_eliminate()
        temp = []
        for direct in self.direct_states:
            logging.debug('direct=%s %s' % (direct, self.direct_states[direct]))
            temp.extend(self.direct_states[direct])

        if len(temp) == 0:
            return

        result = {}
        for state in temp:
            key = (state.ref_id, state.order)
            if key not in result:
                result[key] = state
            else:
                result[key].indexes.extend(state.indexes)

        for (ref_id, order) in result:
            logging.debug(' %s' % (result[(ref_id, order)]))
        

    def swap_monster(self, one_index, other_index):
        one = self.grid[one_index]
        other = self.grid[other_index]

        other.index = one_index
        one.index = other_index

        self.grid[one_index] = other
        self.grid[other_index] = one

    def best_plan_to_swap(self) -> (CellVO, CellVO):
        """
        找出最佳方案
        :return: (CellVO, CellVO) 需要交换的两个 cell
        """
        cells = self.get_complex_swap_choice()
        if len(cells) == 0:
            monster = self.get_simple_swap_choice()
            logging.debug('the way of find by simple %s' % monster)

            if monster is None:
                logging.info("can't find any swap")
            else:
                other_monster = self.get_completion_one(monster)
                return monster, other_monster
            return ()

        if len(cells) > 1:
            first_cell = None
            out_ref_id = None

            for cell in cells:
                # TODO can group by count, then compare all in order final find best choice
                logging.debug('plan: %s expect in:%s actual out:%s count:%s'
                              % (cell.index, cell.ref_id, self.grid[cell.index].ref_id, cell.count))
                if first_cell is None:
                    first_cell = cell
                    out_ref_id = self.grid[cell.index].ref_id
                    continue

                if out_ref_id == cell.ref_id and not self.is_intersect(first_cell, cell):
                    return first_cell, cell

        first = cells[0]
        cell = self.get_completion_one(first)
        logging.debug('get one %s' % cell)
        if cell is not None:
            return first, cell

        return ()

    def is_intersect(self, a, b) -> bool:
        cell_a = self.get_nearby_index_lists(a)
        cell_b = self.get_nearby_index_lists(b)
        logging.debug('%s %s | %s %s' % (cell_a, b.index, a.index, cell_b))

        temp = []
        for indexes in cell_a:
            temp.extend(indexes)
        if b.index in temp:
            return True

        temp = []
        for indexes in cell_b:
            temp.extend(indexes)
        if a.index in temp:
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

    def get_completion_one(self, cell) -> Monster:
        """
        first find in outside , then find min count inside
        :param cell:
        return monster
        """
        index_lists = self.get_nearby_index_lists(cell)
        temp = []
        for indexes in index_lists:
            temp.extend(indexes)

        target = []
        for monster in self.grid:
            if monster.get_type() != CellType.MONSTER:
                continue
            if not monster.is_same(cell):
                continue

            if monster.index in temp:
                logging.debug('ignore %s' % monster)
            else:
                logging.debug('monster=%s' % monster)
                target.append(monster)
        if len(target) != 0:
            return random.choice(target)

    def get_simple_swap_choice(self) -> Monster:
        temp = []
        for direct in self.probably_eliminate:
            state_list = self.probably_eliminate[direct]
            for state in state_list:
                if len(state.indexes) > 1:
                    if state.get_pre(self) is not None:
                        temp.append(self.grid[state.get_pre(self)])
                    if state.get_next(self) is not None:
                        temp.append(self.grid[state.get_next(self)])
                for monster in temp:
                    if monster.get_type() == CellType.MONSTER:
                        return monster
                temp = []

    # 获取备选方案 按权重倒序排序
    def get_complex_swap_choice(self) -> [CellVO]:
        self.check_eliminate()

        result = []
        result.extend(self.cell_vo_by_successive())
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

    def get_repeated_indexes(self, ref_id, vo_tuple) -> [CellVO]:
        temp = {}  # ref_id_order->count
        result = []
        for order, index in vo_tuple:
            base = 1
            if index < 0:
                index *= -1
                base = 1 / 8

            key = (order, index)
            if key not in temp:
                temp[key] = base
            else:
                temp[key] = temp[key] + base

        for order, index in temp:
            key = (order, index)
            if temp[key] > 0.75 and self.grid[index].get_type() == CellType.MONSTER:
                cell = CellVO(ref_id, order, index, temp[key])
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
