from domain.cell_vo import CellVO
from util.logger import log


def best_plan_to_swap(grid) ->(CellVO, CellVO):
    cells = grid.get_complex_swap_choice()
    log.debug('swap choice %s' % cells)
    if len(cells) == 0:
        monster = grid.get_simple_swap_choice()
        log.debug('the way of find by simple %s' % monster)

        if monster is None:
            log.info("can't find any swap")
        else:
            other_monster = grid.get_completion_one(monster)
            return monster, other_monster
        return ()

    if len(cells) > 1:
        max_effect = 0
        cell_tuple = ()
        for i in range(len(cells)):
            for j in range(i + 1, len(cells) - 1):
                log.debug('%s <-> %s' % (cells[i], cells[j]))
                temp = grid.calculate_swap_effect(cells[i].index, cells[j].index)
                if max_effect < temp:
                    max_effect = temp
                    cell_tuple = cells[i], cells[j]
        if max_effect != 0:
            return cell_tuple

    first = cells[0]
    cell = grid.get_completion_one(first)
    log.debug('get one %s' % cell)
    if cell is not None:
        log.debug('random other to eliminate')
        return first, cell

    return ()

