import redis

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
        print(key, data_type)
        data_type = data_type.decode('utf-8')

        if data_type == "string":
            target.set(key, origin.get(key))
        if data_type == "list":
            target.lpush(key, origin.lrange(key, 0, -1))
        if data_type == "set":
            target.sadd(key, origin.smembers(key))
        if data_type == "hash":
            keys = origin.hkeys(key)
            for element in keys:
                target.hset(key, element, origin.hget(key, element))
        else:
            print("未知数据类型")
        count = count+1
            
    print("总共迁移key：", count)

def main():
    origin  = get_connection("120.25.203.47", 6380, "myth", 0 )
    target = get_connection("118.31.14.157", 6379, "myth123", 0 )
    trans(origin, target)
    # trans(target, origin)

main()
