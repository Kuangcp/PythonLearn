import redis


# 转换key value

def get_connection(host, port, password, db):
    return redis.Redis(host, port, db, password)

def trans():
    origin  = get_connection("120.25.203.47", 6380, "myth", 0)
    keys = origin.hkeys("type_dict")
    for key in keys:
        origin.hset("type_dict", origin.hget("type_dict", key), key)
        origin.hdel("type_dict", key)


def main():
    trans()
    pass

main()