"""
    冒泡排序， 时间复杂度是 O(n(n-1)) 空间复杂度是 n
"""


def sort(data):
    """ 冒泡排序 从小到大 """
    for i in range(1, len(data) - 1):  # 外层循环，整体下沉一个大数
        for j in range(0, len(data) - i):  # 每次进行的比较，起始0，终点是未排序的的数
            if data[j] > data[j + 1]:  # 前比后大就交换
                temp = data[j + 1]
                data[j + 1] = data[j]
                data[j] = temp
    return data


def name() -> str:
    return "bubble"
