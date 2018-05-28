##!web_redis_lib/bin/python
from flask import *
from flask_cors import CORS
from base.RedisConfig import RedisConfig
from base.ResultVO import ResultVO as vo
# from module.string import test


class MainConfig:
    def __init__(self, redis):
        self.redis = redis


app = Flask(__name__)
CORS(app, supports_credentials=True)
config = MainConfig(None)
redis = config.redis
# redis = RedisConfig('127.0.0.1', 6666, '', 0).getConnection()

prefix = '/todo/api'
version = 'v1.0'
url = prefix + '/'+version

@app.route(url+'/keys', methods=['GET'])
def list_keys():
    list = redis.keys()
    result = []
    for one in list:
        result.append(one.decode())
    return vo.datas(result)

@app.route(url+'/keys/<int:len>', methods=['GET'])
def list_keys_by_len(len):
    list = redis.keys('?'*len)
    result = []
    for one in list:
        result.append(one.decode())
    return vo.datas(result)

@app.route(url+'/key/<string:key>', methods=['GET'])
def get_key(key):
    re = redis.type(key).decode()
    if re == 'string':
        result = redis.get(key)
        if result != None:
            return vo.one_data(result.decode())
        else:
            return vo.fail(404)
    else:
        return vo.fail(405)

@app.route(url+'/show_code', methods=['GET'])
def show_code():
    list = {
        '404': "资源找不到",
        '405': "键类型错误",
        '406': "参数缺失"
    }
    return vo.datas(list)

#  TODO  如何处理这个redis连接问题
@app.route(url+'/init_redis', methods=['POST'])
def init_redis():
    if not request.json or not 'host' in request.json or not 'port' in request.json or not 'password' in request.json or not 'db' in request.json:
        return vo.fail(406)
    redis = RedisConfig(request.json['host'], request.json['port'], request.json['password'], request.json['db']).getConnection()
    update_redis(redis)
    return vo.success()

def update_redis(redis):
    redis = redis

if __name__ == '__main__':
    app.run(debug=True, port=22334)