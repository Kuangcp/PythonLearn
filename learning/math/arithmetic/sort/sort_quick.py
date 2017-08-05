'''
    快速排序： 建立左右指针位， 先右边比较，将右边的最高位和 参照值比较， 比参照值大就交换，比参照值小就高位指针下移，
        移动到当低位和高位指针相等就退出比较循环，并且进入左边比较的过程，
            如果由于指针位相等的原因左边过程的代码也不会运行，所以要重置高位指针
        左边比较就是一样的， 左边指针的移动。。。
        等左边也运行完了就进入下一轮循环 直至 低位指针和高位指针相遇，就进入递归
     
        
'''
def quick(data):
    return sort(data, 0, len(data)-1)

def sort(data, low, high):
    index_low = low
    index_high = high
    povit = data[low]
    # print('函数入口',index_low, index_high, low, high, data)

    while index_low < index_high:
        povit = data[index_low] # 更新参照指针位
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
        # print(index_low, index_high, data)
        index_low += 1
        # 为什么要把指针高位恢复成入参初始的高位
        index_high = high
    if index_low > low:
        sort(data, low, index_low-1)
    if index_high > high:
        sort(data, index_low+1, high)
    return data