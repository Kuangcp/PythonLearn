from domain.direct_type import DirectType


def is_same_row(a, b, grid) -> bool:
    return int(a / grid.col) == int(b / grid.col)


# 连续的结构
class CellState:
    def __init__(self, ref_id, indexes, order, direct_type):
        self.ref_id = ref_id
        self.order = order
        self.indexes = indexes
        self.direct_type = direct_type
        self.pre = None
        self.next = None

    def __repr__(self) -> str:
        return str(self.ref_id) + ' ' + str(self.indexes)

    def get_pre(self, grid):
        if self.pre is not None:
            return self.pre
        self.calculate_pre_and_next(grid)
        return self.pre

    def get_next(self, grid):
        if self.next is not None:
            return self.next
        self.calculate_pre_and_next(grid)
        return self.next

    def calculate_pre_and_next(self, grid):
        if len(self.indexes) == 0:
            return

        head = self.indexes[0]
        tail = self.indexes[-1]

        if self.direct_type == DirectType.NORTH_EAST:
            self.calculate_north_east(grid, head, tail)
        elif self.direct_type == DirectType.SOUTH_EAST:
            self.calculate_south_east(grid, head, tail)
        elif self.direct_type == DirectType.SOUTH:
            self.calculate_south(grid.col, grid)
        elif self.direct_type == DirectType.EAST:
            self.calculate_east(grid, head, tail)

    def calculate_east(self, grid, head, tail):
        base = 1
        if len(self.indexes) == 1:
            base = -1
        pre = head - 1
        if pre > 0 and is_same_row(pre, head, grid):
            self.pre = pre * base
        next_ = tail + 1
        if next_ < grid.row * grid.col and is_same_row(next_, tail, grid):
            self.next = next_ * base

    def calculate_south_east(self, grid, head, tail):
        base = 1
        if len(self.indexes) == 1:
            base = -1
        if head % grid.col != 0:
            pre = head - (grid.col + 1)
            if pre > 0:
                self.pre = pre * base
        if tail % grid.col != grid.col - 1:
            next_ = tail + grid.col + 1
            if next_ < grid.row * grid.col:
                self.next = next_ * base

    def calculate_north_east(self, grid, head, tail):
        base = 1
        if len(self.indexes) == 1:
            base = -1
        if head % grid.col != grid.col - 1:
            pre = head - (grid.col - 1)
            if pre > 0:
                self.pre = pre * base
        if tail % grid.col != 0:
            next_ = tail + grid.col - 1
            if next_ < grid.row * grid.col:
                self.next = next_ * base

    def calculate_south(self, delta, grid):
        base = 1
        if len(self.indexes) == 1:
            base = -1
        pre = self.indexes[0] - delta
        if pre > 0:
            self.pre = pre * base
        next_ = self.indexes[-1] + delta
        if next_ < grid.row * grid.col:
            self.next = next_ * base
