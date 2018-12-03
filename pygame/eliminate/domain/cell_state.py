from domain.direct_type import DirectType


def is_same_row(a, b, grid) -> bool:
    return int(a / grid.col) == int(b / grid.col)


class CellState:
    def __init__(self, ref_id, indexes, direct_type):
        self.ref_id = ref_id
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
        if self.direct_type == DirectType.NORTH_EAST:
            self.calculate_common(grid.col - 1, grid)
        elif self.direct_type == DirectType.SOUTH_EAST:
            self.calculate_common(grid.col + 1, grid)
        elif self.direct_type == DirectType.SOUTH:
            self.calculate_common(grid.col, grid)
        elif self.direct_type == DirectType.EAST:
            base = 1
            if len(self.indexes) == 1:
                base = -1

            pre = self.indexes[0] - 1
            if pre > 0 and is_same_row(pre, self.indexes[0], grid):
                self.pre = pre * base
            next_ = self.indexes[-1] + 1
            if next_ < grid.row * grid.col and is_same_row(next_, self.indexes[-1], grid):
                self.next = next_ * base

    def calculate_common(self, delta, grid):
        base = 1
        if len(self.indexes) == 1:
            base = -1
        pre = self.indexes[0] - delta
        if pre > 0:
            self.pre = pre * base
        next_ = self.indexes[-1] + delta
        if next_ < grid.row * grid.col:
            self.next = next_ * base
