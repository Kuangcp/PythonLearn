import sort.sort_insert as insert

'''
    TimSort python列表内置的就是该算法的实现:
        结合了合并排序和插入排序得到的算法

    TimSort 算法为了减少对升序部分的回溯和对降序部分的性能倒退，将输入按其升序和降序特点进行了分区。排序的输入的单位不是一个个单独的数字，
    而是一个个的块-分区。其中每一个分区叫一个run。针对这些 run 序列，每次拿一个 run 出来按规则进行合并。
    每次合并会将两个 run合并成一个 run。合并的结果保存到栈中。合并直到消耗掉所有的 run，这时将栈上剩余的 run合并到只剩一个 run 为止。
    这时这个仅剩的 run 便是排好序的结果。

    综上述过程，Timsort算法的过程包括
    （0）如何数组长度小于某个值，直接用二分插入排序算法
    （1）找到各个run，并入栈
    （2）按规则合并run


    第一步就是把待排数组划分成一个个run，当然run不能太短，如果长度小于minrun这个阈值，则用插入排序进行扩充。
    第二步将run入栈，当栈顶的run的长度不满足下列约束条件中任意一个时，
    1. runLen[n-2] > runLen[n-1] + runLen[n]
    2. runLen[n-1] > runLen[n]
    则利用归并排序将其中最短的2个run合并成一个新run，最终栈空的时候排序也就完成了。
'''


def sort(data):
    return data


def name() -> str:
    return "tim"
