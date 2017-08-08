import sys
import disjoint as gather
import random
from time import sleep
'''
    创建迷宫：
        从各处的墙壁开始（除出入口外）， 此时，不断的随机选择一面墙，如果该墙分隔的单元彼此不连通，就把墙拆掉
        重复拆墙， 直到出口所在集合和入口所在集合 连通，就得到一个迷宫了
        
        如果不断的拆墙，直到每一个单元都可以从每个单元连通就会更好，使得迷宫产生更多的迷惑路径

        特别版：
            起初没有起点到终点的连通，拆除预先指定的一面墙（多个之一）后生成一条唯一的路径
'''
def finish(father, start, end):
    ''' 判断开始集和结束集是否相交 ''' 
    return gather.find_pathcompress(father, start) == gather.find_pathcompress(father, end)

def destroy_line(data, father, width, height, index=None, where=None):
    # print(index, where)
    # TODO 需要增加一个条件，就是已经连通的两个节点，就不继续拆墙了，不然到后面墙全没了
    index = random.randint(0, width*height-1)
    where = random.randint(1,6)%2 # 0 1 下 右
    print('位置：',index, '墙：',where)
    # 将随机出来的那面墙消除
    if data[index][1][where] == 0 :
        return 0
    data[index][1][where] = 0
    print(data)
    if where == 0: # 下面的墙销毁,当前和下节点连通
        print('下', index, index+width)
        if index+width <= len(data)-1 :
            gather.union_by_size(father,index, index+width)
    else:
        print('右', index, index+width)
        if not (index+1) % width == 0:
            gather.union_by_size(father,index, index+1)
    print(father)

def show_result(data):
    ''' 展示结果 '''
    pass
def main():
    # sys.setrecursionlimit(100000)
    try:
        max_width = int(sys.argv[1])
        max_height = int(sys.argv[2])
        print('宽 × 高：',max_width, max_height)
    except IndexError:
        print('请输入宽高两个参数在文件后')
        sys.exit(1)
    # 初始化一个完整的墙的地图，放数据是为了以后还能放道具
    # [1,[1,1]] 是一个单元格 1，1 表示下右有墙 width * height 大小的地图
    data = []
    for h in range(0, max_height):
        for d in range(0, max_width):
            data.append([h*max_width+d, [1,1]])
    data[len(data)-1][1] = [0,0]
    print('初始化',data)
    father = [-1 for x in range(len(data))]
    while True:
        sleep(0.3)
        destroy_line(data, father, max_width, max_height)
        if finish(father, max_width-1, len(data)-max_width):
            break

    print('结果是',father)
main()