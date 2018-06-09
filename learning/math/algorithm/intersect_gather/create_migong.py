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
    index = random.randint(0, width*height-1)
    where = random.randint(1,6)%2 # 0 1 下 右
    # 已经连通的节点就不去做并操作了，并且将特殊的最右边，最下边的节点进行处理
    if where == 0:
        if index+width > len(data)-1: # 当是最后一行就不要考虑并操作了
            return 0
        if gather.check_disjoint(father, index, index+width):
            return 0
    else:
        if (index+1) % width == 0:
            return 0
        if gather.check_disjoint(father, index, index+1):
            return 0
    # print('位置：',index, '墙：',where)
    # 将随机出来的那面墙消除
    if data[index][1][where] == 0: # 已经是墙
        return 0
    data[index][1][where] = 0
    # print(data)
    if where == 0: # 下面的墙销毁,当前和下节点连通，前面做了最后一行的判断
        # print('下', index, index+width)
        gather.union_by_size(father,index, index+width)
    else:
        # print('右', index, index+width)
        gather.union_by_size(father,index, index+1)
    # print(father)

def show_result(data, width, height, start, end):
    ''' 展示结果 ''' 
    print('_'*(width*2-1))
    for h in range(height):
        print('|', end="")
        for w in range(width):
            index = h*width+w
            if index!=end and (data[index][1][0] == 1 or index//width == (height-1)):
                print('_', end="")
            else:
                print(' ', end="")
            if data[index][1][1] == 1:
                print('|', end="")
            elif  w != width-1:
                print('_', end="")
        print()

def main():
    try:
        max_width = int(sys.argv[1])
        max_height = int(sys.argv[2])
        print('\n\n宽 × 高：',max_width, '×', max_height)
        print('默认入口在右上角，出口在左下角')

    except IndexError:
        print('请输入宽高两个参数 例如: python3 create_migong.py 20 20 ')
        sys.exit(1)
    
    # 初始化一个完整的墙的地图，放数据是为了以后还能放道具
    # [1,[1,1]] 是一个单元格 1，1 表示下右有墙 width * height 大小的地图
    data = []
    for h in range(0, max_height):
        for d in range(0, max_width):
            data.append([h*max_width+d, [1,1]])
    
    # print('初始化',data)
    father = [-1 for x in range(len(data))]
    # 地图的开始节点和出口节点
    start_index = max_width-1
    end_index = (len(data)-max_width)
    data[end_index][1] = [0,1] # 将出口节点的底墙去掉， 关于开始就不用担心了，因为算法的原因，是肯定不会鼓励出来的
    
    while True:
        # sleep(0.3)
        destroy_line(data, father, max_width, max_height)
        # 出入口两个集合相交， 运算结束
        if finish(father, start_index, end_index):
            break

    # print('结果是',father)
    # print(start_index, end_index)
    show_result(data, max_width, max_height, start_index, end_index)

main()