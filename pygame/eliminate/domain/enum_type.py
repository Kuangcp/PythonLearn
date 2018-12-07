import random
from enum import Enum

from util.logger import log


class OrderType(Enum):
    E = 1
    D = 2
    C = 3
    B = 4
    A = 5

    def string(self) -> str:
        return str(self).replace('OrderType.', '')

    def up(self):
        if self.value == self.A.value:
            log.warning('want to up than A')
            return self
        return OrderType(self.value + 1)


class CellType(Enum):
    STONE = 0
    MONSTER = 1


class StrategyType(Enum):
    HIGH_ORDER_FIRST = 1


def random_order_type():
    return random.choice(list(OrderType.__members__.values()))


def min_order_type():
    return OrderType(1)
