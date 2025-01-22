import datetime
import sys

'''
    求解斐波那契数列 分别使用递归和循环来做，看时间耗费
        递归太不划算,时间花费在很多没必要的事情上， 只适合用来教学，理解递归 33 就需要1s， 34：2s 35：4s 40：1min
        循环的话始终稳定在1s内，因为时间复杂度是 O(n)
'''


def main():
    n = int(sys.argv[1])
    show = None
    if len(sys.argv) > 2:
        if sys.argv[2] == 's':
            show = True
    print('普通循环')
    print('结果：', structs(run_loop, n, show))
    print('精简循环')
    print('结果：', structs(run_loop_min, n, show))
    print('递归')
    print('结果：', structs(run_digui, n, show))


# 全都以1开始计数

# 使用递归，一不小心就会超出Python的最大递归深度，时间慢，资源耗费高
def run_digui(n, show=None):
    if n <= 2:
        return 1
    else:
        return run_digui(n - 1) + run_digui(n - 2)


# 循环存全部数据，内存耗费太大 慎用
def run_loop(n, show=None):
    if n <= 2:
        return 1
    result = [1, 1]
    for i in range(2, n):
        result.append(result[i - 1] + result[i - 2])
    if not show == None:
        print('输出数列数据:', result)
    return result[n - 1]


# 循环 只存两个数据
def run_loop_min(n, show=None):
    if n <= 2:
        return 1
    result = [1, 1]
    if not show == None:
        print('输出数列数据: [1  1', end="")
    for i in range(2, n):
        result[i % 2] = result[0] + result[1]
        if not show == None:
            print(' ', result[i % 2], end="")

    if not show == None:
        print(']')
    if result[1] > result[0]:
        return result[1]
    else:
        return result[0]


def structs(method, n, show=None):
    start = get_time()
    result = method(n, show)
    get_time(start)
    return result


def get_time(start=None):
    '''得到时间，计算运行时间的函数'''
    now = datetime.datetime.now()
    if not start == None:
        print('耗时', now - start)
    return now


main()
