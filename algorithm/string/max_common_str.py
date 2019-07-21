max_len = 2

# 两个字符串求解最长子串
def max_same_str(one, other) -> str:
    if one is None or other is None:
        return False
    
    one_len = len(one)
    other_len = len(other)

    if one_len < max_len or other_len < max_len:
        return False

    arrays = [[0 for col in range(0, one_len)] for row in range(0, other_len)]
    # print(one_len, other_len, arrays)

    max = 0
    index = 0
    for row in range(0, other_len):
        for col in range(0, one_len):
            # print(one, row, other, col)
            one_c = one[col]
            other_c = other[row]
            
            if one_c == other_c:
                if row == 0 or col == 0:
                    # print(row,col)
                    arrays[row][col] = 1
                else:
                    arrays[row][col] = arrays[row-1][col-1] + 1
                if arrays[row][col] > max:
                    max = arrays[row][col]
                    index = row

    result = one[index - max + 1: index + 1 ]
    print(max, result)

    return result


result = max_same_str('abcf', 'bcfg')
print(result)