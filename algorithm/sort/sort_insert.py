"""
  * 插入法排序，由小到大
  * 最坏的情况就是数列是有序的大到小，那么需要比较和移动 n(n+1)/2 次 时间复杂度是O(n^2)
  *
  * 指针从第二个数开始，后移，发现当前数比前面一个数小就把前面那个数后移，往前比较，知道找到那个数小于当前数为止，
  * 指针后移直至到最后一个
  * 思想是，指针位置之前的数都是有序的
"""


def sort(data):
    """ 插入排序，两两比较，将最小的放在第一个，保持前面的有序性，一个一个的判断 """

    for i in range(1, len(data)):
        # print(data[i])
        j = i - 1
        temp = data[i]
        while j >= 0 and temp < data[j]:
            # 比较，如果是比前面还要小，就将数字往后移动一位。将小的那一位插入到合适位置
            data[j + 1] = data[j]
            j -= 1
        data[j + 1] = temp
    return data


def name() -> str:
    return "insert"
