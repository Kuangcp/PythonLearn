import random
from enum import Enum


def random_order_type():
    return random.choice(list(OrderType.__members__.values()))


def min_order_type():
    return OrderType(1)


class OrderType(Enum):
    E = 1
    D = 2
    C = 3
    B = 4
    A = 5

    def string(self) -> str:
        return str(self).replace('OrderType.', '')

    def up(self):
        return OrderType(self.value + 1)


class CellType(Enum):
    STONE = 0
    MONSTER = 1
