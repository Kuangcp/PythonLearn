
from flask import *
from base.ResultVO import ResultVO as vo
from base.RedisConfig import RedisConfig
from .. import app,redis

# redis = RedisConfig('127.0.0.1', 6666, '', 0).getConnection()
# def get_key (key):
#     result = redis.get(key)
#     if result != None:
#         return vo.one_data(result.decode()).jsonify()
#     else:
#         return vo.fail(404).jsonify()
# print(get_key('a'))

url = '/redis/api/v1.0'

@app.route(url+'/key', methods=['POST'])
def set_key(key):
    re = redis.type(key)
    if re == b'string':
        result = redis.get(key)
        if result != None:
            return vo.one_data(result.decode())
        else:
            return vo.fail(404)
    else:
        return vo.fail(405)

