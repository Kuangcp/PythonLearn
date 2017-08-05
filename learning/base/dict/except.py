import redis
from redis import Redis

# while True:
#     a = input("first")
#     b = input("second")
#     try:
#         print(int(a) / int(b))
#     except ZeroDivisionError:
#         print("0 不能做除数")
#     else:
#         print("成功")

conn = redis.Redis(host='120.25.203.47', port=6379, db=0, password='myth')
conn.set('d', 'd12121212121212')
f = conn.get('d')
print(str(f))