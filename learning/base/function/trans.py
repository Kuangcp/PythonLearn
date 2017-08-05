'''
    列表是和类c语言的数组一样是传递引用的
'''

def run(data):
    # print('89')
    data.append(78)
    data.append(898989)

    temp = data[0]
    data[0] = data[1]
    data[1] = temp

def main():
    data = [5, 6, 12, 34, 3, 8, 1]
    run(data)
    print(data)
    lists = [0 for x in range(0, len(data))]
    print(data)

main()
