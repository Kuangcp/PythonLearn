
# 递归和尾递归的对比

def simple(n):
    ''' 最简单的递归方式来计算阶乘'''
    if n == 1:
        return 1
    else:
        return n * simple(n-1)

def factorial(n, result=1):
    ''' 尾递归, 将结果带入到下一次方法调用'''
    if n == 1:
        return result;
    else:
        return factorial(n-1, n*result)

num = 10
print(factorial(num))
print(simple(num))

# TODO 如何优化, 跳出Python对递归深度的限制