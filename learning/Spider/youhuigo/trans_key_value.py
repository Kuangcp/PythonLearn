import redis


# 交换key value

def get_connection(host, port, password, db):
    return redis.Redis(host, port, db, password)

def trans():
    origin  = get_connection("120.25.203.47", 6380, "myth", 0)
    keys = origin.hkeys("type_dict")
    for key in keys:
        origin.hset("type_dict", origin.hget("type_dict", key), key)
        origin.hdel("type_dict", key)


def delete_head():
    ''' 补救，删除头信息，太慢，还不如跳转逻辑修改'''
    origin = get_connection("118.31.14.157", 6379, "myth123", 0)
    indexs = origin.hkeys("short_index")
    count = 0
    counts = 0
    # for ids in indexs:
    #     short_link = origin.hget("short_index", ids).decode()
    #     # print(short_link)
    #     if short_link.startswith("http://"):
    #         counts = counts + 1
    #         print(counts)
    # print("------"+counts)
    for ids in indexs:
        short_link = origin.hget("short_index", ids).decode()
        # print(short_link)
        if short_link.startswith("http://"):
            count = count + 1
            long_link = origin.hget("short_map", short_link).decode()
            origin.hdel("short_map", short_link)
            # print(ids, short_link)
            short_link = short_link.split("/")[-1]
            # print(short_link)
            origin.hset("short_map", short_link, long_link)
            origin.hset("short_index", ids, short_link)
            print(count)
        # if count == 100:
        #     return 0



def main():
    # trans()
    delete_head()


main()