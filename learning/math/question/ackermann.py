'''
    ackermann 算法  递归狂魔
    http://www.cnblogs.com/jjtx/archive/2012/03/07/2533508.html
    http://hi.csdn.net/attachment/201203/7/0_13311132738CB3.gif

    public static long ackermann(long m, long n) {
        return (m==0)?
                n+1:
                (m>0 && n==0)?
                    ackermann(m-1,1):
                    ackermann(m-1, ackermann(m,n-1)); 
    }
'''


def ackermann(m, n):
    if m == 0:
        return n + 1
    if m > 0 and n == 0:
        return ackermann(m - 1, 1)
    else:
        return ackermann(m - 1, ackermann(m, n - 1))


print(ackermann(4, 1))
