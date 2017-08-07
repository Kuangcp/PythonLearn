import datetime
import random
import sys

import sort_box as box
import sort_bubble as bubble
import sort_insert as insert
import sort_select as select
import sort_shell as shell
import sort_merge as merge
import sort_quick as quick

'''
    参数： [数量] [范围][排序类别][c 检查/s 展示]

    结论： 在效率上，箱排序，归并排序,快速排序 是同等级比较好的排序方法，
        快速一般要快于归并（如果数据大量重复就会慢，归并不受影响）
    
'''

def main():
    '''统一测试所有的排序算法''' 
    sort_size = 10
    max_num = 100000
    detail = False # 是否输出具体数据
    check = False # 是否检查排序结果

    flag_bubble = False
    flag_box = False
    flag_insert = False
    flag_select = False
    flag_shell = False
    flag_merge = False
    flag_quick = False
    flag_all = True # 如果没有指定排序就是全部

    # 得到参数，如果是 python main.py s c 就输出数据信息并且检查排序结果
    if len(sys.argv) > 1:
        try:
            sort_size = int(sys.argv[1])
            max_num = int(sys.argv[2])
        except ValueError:
            print("默认长度10 100000")
        for param in sys.argv:
            # print(param, len(param))
            # 如果参数中有两位的，说明是指定的排序，就不要全运行了
            if len(param) == 2 and not isinstance(param, int):
                flag_all = False
                
            if param == 's':
                detail = True
            if param == 'c':
                check = True
            if param == 'bu':
                flag_bubble = True
            if param == 'bo':
                flag_box = True
            if param == 'in':
                flag_insert = True
            if param == 'se':
                flag_select = True
            if param == 'sh':
                flag_shell = True
            if param == 'me':
                flag_merge = True
            if param == 'qu':
                flag_quick = True
            
    # 如果没有指定参数就默认是全部排序运行
    if flag_all:
        flag_bubble = flag_box = flag_insert = flag_select = flag_shell = flag_merge = flag_quick = True
    
    # 生成随机数据
    origin_data = [random.randint(1, max_num) for x in range(sort_size)]
    print('排序的数据数量： [', sort_size, ']  数据范围： [ 0 -', max_num, ']\n')
    show_list(origin_data, '-'*10+'得到原始数据', detail)# 由参数确定书否输出

    # 开始排序
    
    if flag_box:
        run_sort(box.box, origin_data, '箱排序', detail, check)
    if flag_merge:
        run_sort(merge.merge, origin_data, '归并排序', detail, check)
    if flag_quick:
        run_sort(quick.quick, origin_data, '快速排序', detail, check)
    if flag_insert:
        run_sort(insert.insert, origin_data, '插入排序', detail, check)
    if flag_select:
        run_sort(select.select, origin_data, '选择排序', detail, check)
    if flag_bubble:
        run_sort(bubble.bubble, origin_data, '冒泡排序', detail, check)
    if flag_shell:
        run_sort(shell.shell, origin_data, '希尔排序', detail, check)
    
    

def run_sort(function, origin_data, title, detail, check):
    ''' 
        全部的排序算法在这里封装，加入时间和正确性检测
    '''
    if not title == None:
        print('-'*30+' 开始'+title+' '+'-'*(35-len(title)))
    result_title = '排序后的结果：' # 排序结果输出的标题
    data = origin_data[:] # 复制数据，为了不影响其他排序算法
    start = get_time()
    result_data = function(data)
    get_time(start)
    show_list(result_data, result_title, detail, check)

def show_list(data, title, show=True, check=False):
    '''输出数据，以及校验数据'''
    # 不显示具体数据但是要检查
    if check:
        success = True
        for i in range(1, len(data)):
            # print(data[i-1],data[i],data[i-1]>data[i])
            if data[i-1]>data[i]:
                success = False
                break
        if success:
        #    print("<<<  排序结果完全正确  >>>")
            print('>>> OK !')
        else:
            print('！！！算法编写错误！！！')
        #    return 0
             
    # 不显示具体数据的输出
    if not show: 
        return 0
    
    print(title)
    line = ''
    for temp in range(0, len(data)):
        line += str(data[temp])+'  '
        if temp % 23 == 23:
            print(line)
            line = ''
    print(line)



def get_time(start=None):
    '''得到时间，计算运行时间的函数'''
    
    now = datetime.datetime.now()
    if not start == None:
        print('排序耗时', now - start)
    return now

main()
