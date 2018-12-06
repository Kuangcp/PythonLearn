
# 递归和尾递归的对比, 无论是何种方式都会被Python的递归深度限制

def simple(n):
    ''' 最简单的递归方式来计算阶乘'''
    if n == 1:
        return 1
    else:
        return n * simple(n-1)

def factorial(n, result=1):
    ''' 尾递归, 直接返回函数'''
    if n == 1:
        return result
    else:
        return factorial(n-1, n*result)

num = 1000
print(factorial(num))
print(simple(num))

# TODO 如何优化, 跳出Python对递归深度的限制
