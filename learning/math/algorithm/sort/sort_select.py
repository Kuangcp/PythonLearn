'''
    * 选择排序，小到大
    * 原理是：第一个依次与后面所有元素进行比较，遇到比自己小的就交换直到最后，第二轮就拿第二个元素去依次比较
    * 最坏的情况是： 时间复杂度是O(n^2) 比较和交换 n(n-1)/2 次
'''

def select(data):
    size = len(data)
    for i in range(0, size):
        for j in range(i+1, size):
            if data[i] > data[j]:
                temp = data[i]
                data[i] = data[j]
                data[j] = temp
    return data