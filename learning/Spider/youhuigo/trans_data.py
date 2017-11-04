import redis
# import MySQLdb

'''
    脚本实现redis数据迁移
'''

def get_connection(host, port, password, db):
    return redis.Redis(host, port, db, password)

def trans(origin, target):
    origin_data = origin.keys()
    count = 0
    for key in origin_data:
        data_type = origin.type(key)
        
        data_type = data_type.decode('utf-8')
        print(key, data_type)
        if data_type == "string":
            target.set(key, origin.get(key))
        elif data_type == "list":
            target.lpush(key, origin.lrange(key, 0, -1))
        elif data_type == "set":
            values = origin.smembers(key)
            for value in values:
                target.sadd(key, value)
        elif data_type == "zset":
            for value, score in origin.zrange(key, 0, -1, withscores=True):
                target.zadd(key, value, score)
        elif data_type == "hash":
            keys = origin.hkeys(key)
            for element in keys:
                target.hset(key, element, origin.hget(key, element))
        else:
            print("未知数据类型")
        count = count+1
            
    print("总共迁移key：", count)

# def trans_mysql():
#     pass

def main():
    # redis之间进行数据迁移
    origin  = get_connection("120.25.203.47", 6380, "myth", 0 )
    # target = get_connection("127.0.0.1", 6379, None, 0 )
    target = get_connection("118.31.14.157", 6379, "myth123", 0 )
    trans(origin, target)
    # trans(target, origin)
    pass

main()
