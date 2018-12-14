'''
    厄拉多塞筛 是一种计算小于N的所有素数的方法：
        先得到一个2-N的列表，然后从最小的整数i开始，删除i，2i, 3i...... 当 i > 根号N 算法终止
'''
def erastothenes(n):
    if n <= 1:
        print('没有符合条件的素数')
        return 0
    elif n <= 2:
        print('2')
        return 0
    lists = [i for i in range(2, n)]
    while lists[0] <= n and len(lists)>=1:
        low = temp = lists[0]
        print(low,' ', end="")
        if len(lists) == 1:
            break
        i = 2
        while temp < n:
            try:
                lists.remove(temp)
            except ValueError:
                # 如果找不到该元素，就跳过，因为有多个因子的数存在
                pass
            temp = i * low
            i += 1
    print()
erastothenes(int(input("请输入值")))