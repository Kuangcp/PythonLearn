from domain.enum_type import CellType


class Monster:
    def __init__(self, index, ref_id, order, count):
        self.index = index
        self.ref_id = ref_id
        self.order = order  # 品质
        self.count = count  # 数量

    def __repr__(self) -> str:
        return 'monster: index=%s ref_id=%s order=%s count=%s' % (self.index, self.ref_id, self.order.string(), self.count)

    @staticmethod
    def get_type():
        return CellType.MONSTER

    def show(self) -> str:
        return '[' + self.ref_id + ',' + self.order.string() + ',' + str(self.count) + ']'

    def simple_show(self):
        return self.ref_id

    def is_same(self, target) -> bool:
        return self.ref_id == target.ref_id and self.order == target.order
