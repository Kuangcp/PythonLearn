import math
'''
    堆(优先队列) 建立在完全二叉树上 使用列表存储，第一个元素是标识元素，真正从1开始是堆
    小顶堆： i <= 2*i 且 i<2*i+1 即父节点大于等于左右子节点
    大顶堆： 相反
    这里我使用小顶堆
'''
def insert(heap, value):
    ''' 将元素插入堆中 上滤'''
    heap.append(0) # 增加长度
    index_parent = int((len(heap) - 1) / 2) # 长度的一半就是父节点
    index_space = len(heap) - 1
    # print(index_parent, index_space, value, heap)
    while index_space >= 1:
        # 如果父节点比新值大，且父节点大于等于1（为了留个数组第一项出来）
        if heap[index_parent] > value and index_parent >= 1:
            heap[index_space] = heap[index_parent]
            index_space = index_parent
            index_parent = int(index_space/2)
        else:
            heap[index_space] = value
            break

def check_heap(heap):
    ''' 比较堆的有序性 '''
    flag = True
    # start = int(len(heap)/8)
    while flag:
        flag = False
        for i in range(2, len(heap)): 
            # 原本从2开始，对完整堆进行检查，现在只检查三层 提高 20% 左右效率但是会时不时出现bug
            # 因为，如果是子节点填充父节点，只会可能导致这两层乱序，如果是相邻子节点填充当前父节点就有可能导致三层乱序
            if (heap[i] < heap[int(i/2)]):
                flag = True
                temp = heap[i]
                heap[i] = heap[int(i/2)]
                heap[int(i/2)] = temp

def delete_min(heap):
    if len(heap)==3:
        if heap[1] < heap[2]:
            return heap.pop(1)
        return heap.pop()
    elif len(heap) == 2:
        return heap.pop()
    elif len(heap) == 1:
        return None
    
    result = heap[1]
    
    # 重建式，效率更低
    # heap[1] = heap.pop()
    # heap.pop(0)
    # heap = build_heap(heap)
    # print(heap)
    
    # 下滤
    # 将第一个和最后一个踢出，层层往下比较，填充直到最后一层，然后将最后一个已经填充的数放入最后一个值
    key = heap.pop() # 最后一个弹出
    space = 1
    while 2*space+1 <= len(heap)-1:
        # print('空白',space, len(heap))
        if heap[space * 2] < heap[space * 2 + 1]:
            heap[space] = heap[space * 2]
            space = 2 * space
        else:
            heap[space] = heap[space * 2 + 1]
            space = space * 2 + 1
    # 空到最后一层时，填充进已经填充好了的数，若发现填充破坏了堆的有序性，就交换
    heap[space] = key
    check_heap(heap)
    # print('运算结束',heap,space)
    return result

def build_heap(data):
    ''' 构建堆返回一个新列表 '''
    heap = [0]
    for ele in data:
        insert(heap, ele)
    return heap

def decreaseKey():
    ''' 降低关键字的值， 降低处在指定位置的值 上滤操作'''    
    pass
def increaseKey():
    ''' 增加关键字的值， 增加处在指定位置的值 下滤操作'''
    pass
def delete():
    ''' 先decreaseKey上滤到顶层，然后delete'''
    pass
