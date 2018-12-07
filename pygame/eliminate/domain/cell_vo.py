class CellVO:
    def __init__(self, ref_id, order, index, weight):
        self.index = index
        self.ref_id = ref_id  # 期望替换过来的ref_id
        self.order = order  # 期望的order
        self.weight = weight  # 重叠的权重

    def __repr__(self) -> str:
        return 'ref_id=%s index=%s order=%s weight=%s' % (self.ref_id, self.index, self.order.string(), self.weight)
