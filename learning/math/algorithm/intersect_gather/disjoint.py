import random
'''
    不相交的集合下的 union find 算法
'''

def union_by_size(father, root1, root2):
    ''' 必须是两个根节点 按节点数大小来合并 小的合并到大上 使用父节点数组来存放树的大小，负数形式'''
    if father[root1] > 0 or father[root2] > 0:
        return 0
    if father[root1] > father[root2]: # size上 1 比 2 小
        father[root2] = father[root1] + father[root2] # 先把两个根的大小相加
        father[root1] = root2 # root2 成为root1 的父节点
    else:
        father[root1] = father[root1] + father[root2]
        father[root2] = root1


def union_by_height(father, root1, root2):
    if father[root2] < father[root1]:# 如果2更深就把1挂在2下面
        father[root1] = father[root2]
    else:
        if father[root1] == father[root2]:# 相等就要深度加一了
            father[root1] -= 1
        father[root2] = root1


def find(father, index):
    ''' 找到节点的根返回 '''
    # 如果就是根就返回了，如果不是，就递归上溯
    if (father[index] < 0):
        return index
    else:
        return find(father, father[index])

def find_pathcompress(father, index):
    '''
    找到节点的根返回, 路径压缩 就是将第一次递归的结果存起来，每个子节点指向的不是上级节点而是根节点 
    但是这样破坏了树的深度，相当于降维打击了
    '''
    # 如果就是根就返回了，如果不是，就递归上溯
    if (father[index] < 0):
        return index
    else:
        father[index] = find_pathcompress(father, father[index])
        return father[index]

def main():
    data = [random.randint(1,100) for x in range(10)]
    father = [-1 for x in range(len(data))]
    # size = [1 for x in range(len(data))]
    union_by_size(father, 4, 5)
    union_by_size(father, 4, 6)
    union_by_size(father, 4, 7)
    union_by_size(father, 0, 1)
    union_by_size(father, 0, 2)
    union_by_size(father, 0, 3)
    union_by_size(father, 4, 8)
    union_by_size(father, 0, 4)
    print(data, father)
    print(find_pathcompress(father,3))
    print(data, father)


main()
