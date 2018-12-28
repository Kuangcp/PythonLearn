"""
    箱排序，也称桶排序，属于基数排序，其基本思想是：
        设置若干箱子，依次扫描数据， 将关键字等于k的记录全部放入第k箱子， 然后再将箱子首尾连接（收集）
        例如对数值排序,以位数上的数值为键，先0-9十个箱子，只看个位数，排好，连接，
            然后0-9十个箱子十位数， 排好连接，循环直至最大位结束
        那么就要先得到最大数，然后才能确定位数，才能确定循环次数

    优点， 在数据小，量大时排序非常快，需要比较(log10 n)*n次 时间复杂度是O(n) 空间复杂度是2n
"""


def box(data) -> []:
    maxValue = data[0]
    for i in range(1, len(data)):
        if maxValue < data[i]:
            maxValue = data[i]
    length = len(str(maxValue))  # 得到数据最大位数

    for loop in range(1, length + 1):
        data_dict = {}

        for num in data:
            box_type = int((num / (10 ** (loop - 1)))) % 10
            if box_type in data_dict:
                data_dict[box_type].append(num)
            else:
                data_dict[box_type] = [num]

        data = []
        for i in range(10):
            if i in data_dict:
                data.extend(data_dict[i])
    return data
