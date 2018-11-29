class Stone:
    def __init__(self, index, hp):
        self.index = index
        self.hp = hp  # 剩余被消除次数

    def __repr__(self) -> str:
        return 'stone: index=' + str(self.index) + ' hp=' + str(self.hp)

    def show(self) -> str:
        return '[' + str(self.hp) + ']'
