import sys

'''
    快速排序： 建立左右指针位， 先右边比较，将右边的最高位和 参照值比较， 比参照值大就交换，比参照值小就高位指针下移，
        移动到当低位和高位指针相等就退出比较循环，并且进入左边比较的过程，
            如果由于指针位相等的原因左边过程的代码也不会运行，所以要重置高位指针
        左边比较就是一样的， 左边指针的移动。。。
        等左边也运行完了就进入下一轮循环 直至 低位指针和高位指针相遇，就进入递归
     
    一趟快速排序的算法是：
        1）设置两个变量i、j，排序开始的时候：i=0，j=N-1；
        2）以第一个数组元素作为关键数据，赋值给key，即key=A[0]；
        3）从j开始向前搜索，即由后开始向前搜索(j--)，找到第一个小于key的值A[j]，将A[j]和A[i]互换；
        4）从i开始向后搜索，即由前开始向后搜索(i++)，找到第一个大于key的A[i]，将A[i]和A[j]互换；
        5）重复第3、4步，直到i=j； (3,4步中，没找到符合条件的值，即3中A[j]不小于key,4中A[i]不大于key的时候改变j、i的值，
        使得j=j-1，i=i+1，直至找到为止。找到符合条件的值，进行交换的时候i， j指针位置不变。另外，i==j这一过程一定正好是i+或j-完成的时候，此时令循环结束）。
    有问题存在，当数据量达到 20000 就要好久,, ee 是程序的锅，是对算法没理解好
    优缺点： 当数据重复大，就会慢一些
'''


def sort(data):
    sys.setrecursionlimit(100000)  # 设置最大递归深度
    # return sort(data, 0, len(data)-1)
    return quick_sort(data, 0, len(data) - 1)


# 高效无误的写法
def quick_sort(L, low, high):
    i = low
    j = high
    # 不合理的区间不做操作
    if i >= j:
        return L
    key = L[i]
    while i < j:
        # 找出右边小于低位所在的标识值
        while i < j and L[j] >= key:
            j = j - 1
            # print('--',i,j,L)
        L[i] = L[j]
        # print('>=',i,j,L)
        # 找出左边大于标识值
        while i < j and L[i] <= key:
            i = i + 1
            # print('--',i,j,L)
        L[j] = L[i]
        # print('<=',i,j,L)
    L[i] = key
    # print(L)
    quick_sort(L, low, i - 1)
    quick_sort(L, j + 1, high)
    return L


# 低效有bug
def slow_sort(data, low, high):
    index_low = low
    index_high = high
    povit = data[low]
    # print('函数入口',index_low, index_high, low, high, data)

    while index_low < index_high:
        povit = data[index_low]  # 更新参照指针位
        # print('进入左边')
        while index_low < index_high and data[index_high] >= povit:
            # print(index_low, index_high, data[index_high], povit)
            index_high -= 1
        # print(index_low, index_high, data)
        if index_low < index_high:
            temp = data[index_high]
            data[index_high] = data[index_low]
            data[index_low] = temp
            index_low += 1
        # print(index_low, index_high, data)

        # print('进入右边')
        # index_high = high
        while index_low < index_high and data[index_low] <= povit:
            # print(index_low, index_high, data[index_high], povit)
            index_low += 1
        # print(index_low, index_high, data)
        if index_low < index_high:
            temp = data[index_high]
            data[index_high] = data[index_low]
            data[index_low] = temp
            index_high -= 1
        # print('一轮循环结束', index_low, index_high, data)

        # 为什么要把指针高位恢复成入参初始的高位
        if index_low == index_high:
            index_high = high
            index_low += 1
    # print('循环结束', index_low, index_high,'--', low, high, data)
    if index_low > low:
        slow_sort(data, low, index_low - 1)
    if index_high > high:
        slow_sort(data, index_low + 1, high)
    return data


def name() -> str:
    return "quick"
