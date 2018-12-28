import random
import sort.sort_insert as insert

'''
 * shell排序，从小到大
 * 算法思想：
 * 	对一个线性数据，先取一个随机数d1（d1<数据总数）将所有数据分成d组，将所有距离为d倍数的分成一组
 *  对各组进行直接插入排序，然后再取第二个数d2，直到dn=1（dn<……d3<d2<d1）即分成了一组，再插入排序，得出最终结果
 * 时间复杂度：平均：O(n*log n) 最坏 O(n^s)(1<s<2)
 *
 * 实现了算法，但是大量的数据转换，消耗了性能，需要换种思路来实现算法

 优缺点： 希尔，增量序列的选择很重要，分组太多就要需要频繁使用插入排序，不好掌控，
    其中最好的序列是 1,5,19,41,109.... 序列的通项公式是 9*4**i - 9*2**i + 1 或者是 4**i-3*2**i+1
'''


def sort(data):
    size = random.randint(1, len(data))  # 随机分组
    # print('首次分组：',size)
    # 一轮分组
    divide_group(data, size)
    # 不断的将组减小，直至只有一个组
    while not size == 1:
        size = random.randint(1, size - 1)
        # print('分组：',size)
        data = divide_group(data, size)
    return data


def divide_group(data, size):
    temp = []
    for j in range(0, size):
        elem = []
        for i in range(0, len(data)):
            if i % size == j:
                elem.append(data[i])
        elem = insert.sort(elem)
        temp.append(elem)
    data = []
    for group in temp:
        data += group
    return data


def name() -> str:
    return "shell"
