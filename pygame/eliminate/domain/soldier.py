class Soldier:
    def __init__(self, ref_id, order, level, count):
        self.ref_id = ref_id
        self.order = order  # 品质
        self.level = level  # 等级
        self.count = count
        if count < 1:
            self.count = 1
        if level < 1:
            self.level = 1

    def __repr__(self):
        return 'soldier ref_id=%s order=%s level=%s count=%s' \
               % (self.ref_id, self.order.string(), self.level, self.count)
