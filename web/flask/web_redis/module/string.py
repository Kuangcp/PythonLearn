from web_redis.base.ResultVO import ResultVO as vo
from web_redis.base.RedisConfig import RedisConfig

redis = RedisConfig('127.0.0.1', 6666, '', 0).getConnection()
def get_key (key):
    result = redis.get(key)
    if result != None:
        return vo.one_data(result.decode()).jsonify()
    else:
        return vo.fail(404).jsonify()

print(get_key('a'))