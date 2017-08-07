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

def delete_min(heap):
    result = heap[1]
    # 下滤
    key = heap.pop() # 最后一个弹出
    space = 1
    while space<len(heap) - 1:
        if heap[space * 2] < heap[space * 2 + 1]:
            heap[space] = heap[space * 2]
        else:
            heap[space] = heap[space * 2 + 1]
    print(heap)
    return result

def build_heap(data):
    ''' 构建堆 '''
    heap = [0]
    for ele in data:
        insert(heap, ele)
    return heap

def main():
    lists = [1,4,-2,-3,2,0]
    result = build_heap(lists)
    print(result) 
    delete_min(result)

main()
