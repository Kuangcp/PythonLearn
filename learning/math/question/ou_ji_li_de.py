'''
    欧几里得算法，辗转相除求最大公约数:
        假定m >= n： m对n取余，除数作为大数，余数作为小数，继续循环取余
        即使m<n ,循环中也将其交换了
'''

def gcd(m, n):
    while not n == 0:
        temp = m % n
        m = n
        n = temp
    return m

def main():
    print(gcd(6, 9))

main()