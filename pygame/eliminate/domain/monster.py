class Monster:
    def __init__(self, index, ref_id, order):
        self.index = index
        self.ref_id = ref_id
        self.order = order  # 品质

    def __repr__(self) -> str:
        return 'monster: index=' + str(self.index) + ' ref_id=' + str(self.ref_id) + ' order=' + str(self.order)

    def show(self) -> str:
        return '[' + self.ref_id + ',' + str(self.order) + ']'
