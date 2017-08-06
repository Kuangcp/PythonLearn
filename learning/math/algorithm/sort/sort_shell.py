import random
import sort_insert as insert

'''
 * shell排序，从小到大
 * 算法思想：
 * 	对一个线性数据，先取一个随机数d1（d1<数据总数）将所有数据分成d组，将所有距离为d倍数的分成一组
 *  对各组进行直接插入排序，然后再取第二个数d2，直到dn=1（dn<……d3<d2<d1）即分成了一组，再插入排序，得出最终结果
 * 时间复杂度：平均：O(n*log n) 最坏 O(n^s)(1<s<2)
 *
 * 实现了算法，但是大量的数据转换，消耗了性能，需要换种思路来实现算法
 优缺点： 希尔，随机性太大，分组太多就要需要频繁使用插入排序，不好掌控，
 如果把分组在可控的范围内，例如指定分组，归并？
'''


def shell(data):
    size = random.randint(1, len(data)) # 随机分组
    # print('首次分组：',size)
    # 一轮分组
    devide_group(data, size)
    # 不断的将组减小，直至只有一个组
    while not size == 1:
        size = random.randint(1, size-1)
        # print('分组：',size)
        data = devide_group(data, size)
    return data

def devide_group(data, size):
    temp = []
    for j in range(0, size):
        elem = []
        for i in range(0, len(data)):
            if i % size == j:
                elem.append(data[i])
        elem = insert.insert(elem)
        temp.append(elem)
    data = []
    for group in temp:
        data += group
    return data