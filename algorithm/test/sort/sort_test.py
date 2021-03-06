import datetime
import unittest
import random

import sort.sort_radix as radix
import sort.sort_bubble as bubble
import sort.sort_insert as insert
import sort.sort_select as select
import sort.sort_shell as shell
import sort.sort_merge as merge
import sort.sort_quick as quick
import sort.sort_heap as heap

max_num_value = 1000
sort_scale = 100

all_sorts = [radix, bubble, insert, select, shell, merge, quick, heap]


def generate_data():
    return [random.randint(1, max_num_value) for x in range(sort_scale)]


def check_sorted(data) -> bool:
    for i in range(0, len(data) - 1):
        if data[i] > data[i + 1]:
            print('error:', data[i], data[i + 1])
            return False
    return True


def get_time(start=None):
    """得到时间，计算运行时间的函数"""

    now = datetime.datetime.now()
    if start is not None:
        microseconds = (now - start).microseconds
        # print('waste time:', microseconds / 1000, 'ms')
        return microseconds
    return now


class TestSortCorrect(unittest.TestCase):
    """测试排序算法正确性"""

    def test_radix_sort(self):
        result = radix.sort(generate_data())
        assert check_sorted(result)

    def test_bubble_sort(self):
        result = bubble.sort(generate_data())
        assert check_sorted(result)

    def test_heap_sort(self):
        result = heap.sort(generate_data())
        assert check_sorted(result)

    def test_insert_sort(self):
        result = insert.sort(generate_data())
        assert check_sorted(result)

    def test_merge_sort(self):
        result = merge.sort(generate_data())
        assert check_sorted(result)

    def test_quick_sort(self):
        result = quick.sort(generate_data())
        assert check_sorted(result)

    def test_select_sort(self):
        result = select.sort(generate_data())
        assert check_sorted(result)

    def test_shell_sort(self):
        result = shell.sort(generate_data())
        assert check_sorted(result)


class TestPerformance(unittest.TestCase):
    """测试性能"""

    def test_all_sort(self):
        global max_num_value, sort_scale

        max_num_value = 100000000
        sort_scale = 500

        start = get_time()
        data = generate_data()
        waste = get_time(start)
        print('generate data: %s' % waste)

        result = {}
        sort_start = get_time()
        for sort in all_sorts:
            # print('sort: %-7s' % (sort.name()), end='  |')
            target_data = data[:]
            start = get_time()
            sort.sort(target_data)
            result[sort.name()] = get_time(start)

        # TODO 总时间对不上
        print("all sort start: ", get_time(sort_start))

        sort_result = sorted(result.items(), key=lambda d: d[1], reverse=True)
        for key, value in sort_result:
            print('|%-7s  | %s ms' % (key, value / 1000))


if __name__ == '__main__':
    unittest.main()
