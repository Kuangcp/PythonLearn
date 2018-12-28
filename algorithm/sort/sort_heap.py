import sort.heap as heap

'''
    堆排序： 构建堆，不停删除堆顶，然后重建堆，达到排序的目的，
        
    性能略差于其他排序(八种排序中最差的了，可能是受编写的影响)，几乎不受重复数据影响
'''


def sort(data):
    heap_list = heap.build_heap(data)
    # print('得到堆',heap_list)
    data = []
    while True:
        ele = heap.delete_min(heap_list)
        # if len(heap_list) >= 3:
        #     heap_list = heap.build_heap(heap_list)
        if ele is None:
            break
        data.append(ele)
    return data


def name() -> str:
    return "heap"
