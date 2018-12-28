"""
    归并排序：从底向上类型
        二分法向下递归， 然后到底了就开始比较然后排序，再依次向上归并比较排序直至归并成一个
    时间复杂度 O((log2 n)*n) 空间复杂度是 2n 需要一个等大的数组做交换暂存空间
    认为是非常优秀的排序算法，就是要耗空间
"""


def sort(data):
    # 声明一个和原数据一样固定大小的列表先， 初始数据为0    
    lists = [0 for x in range(0, len(data))]
    merge_sort(data, 0, len(data) - 1, lists)
    return data


# 将列表的两部分 进行合并
def merge_list(origin, first, mid, last, target):
    # target = []
    start_a = first
    end_a = mid
    start_b = mid + 1
    end_b = last

    index = first  # 每次的起始都是每次的片段的开头不总是0
    # print(start_a, end_a, start_b, end_b)
    # 相同长度比对合并
    while start_a <= end_a and start_b <= end_b:
        if origin[start_a] < origin[start_b]:
            target[index] = origin[start_a]
            start_a += 1
            index += 1
        else:
            target[index] = origin[start_b]
            start_b += 1
            index += 1
    while start_a <= end_a:
        target[index] = origin[start_a]
        start_a += 1
        index += 1
    while start_b <= end_b:
        target[index] = origin[start_b]
        start_b += 1
        index += 1

    for i in range(first, index):
        origin[i] = target[i]

    # print(origin)
    # return target


def merge_sort(origin, first, last, target):
    # print('first',first,'last',last)
    if first < last:
        mid = int((first + last) / 2)

        merge_sort(origin, first, mid, target)  # 左边有序
        merge_sort(origin, mid + 1, last, target)  # 右边有序
        merge_list(origin, first, mid, last, target)  # 左右合并


def name() -> str:
    return "merge"
