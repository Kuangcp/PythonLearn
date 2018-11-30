from enum import Enum


class OrderType(Enum):
    D = 1
    C = 2
    B = 3
    A = 4
    S = 5

    def string(self) -> str:
        return str(self).replace('OrderType.', '')

    def up(self):
        return OrderType(self.value + 1)

class CellType(Enum):
    STONE = 0
    MONSTER = 1
