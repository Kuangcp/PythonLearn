## !/usr/bin/python3
##!web_redis_lib/bin/python
from base.RedisConfig import RedisConfig
from base.ResultVO import ResultVO as vo

# from module.string import *
from flask import *
from flask_cors import CORS

redis = None
app = Flask(__name__, static_folder='./static')
CORS(app, supports_credentials=True)

# 构造应用基础路径
url = '/redis/api/v1.0'

# url_for方法能得到相对路径
# 检查是否初始化redis
@app.before_request
def check():
    global redis
    path = request.path
    ignore = ['init_redis', 'show_code', 'html', 'css', 'js', 'jpg', 'static/']
    isIgnore = False
    for one in ignore:
        if path.endswith(one):
            isIgnore = True
            break
    if redis == None and not isIgnore:
        return vo.fail(407)
    else:
        redirect(path)

@app.route(url+'/keys', methods=['GET'])
def list_keys():
    list = redis.keys()
    result = []
    for one in list:
        result.append(one.decode())
    return vo.multiple(result)

# 列出所有见, 按键的长度
@app.route(url+'/keys/<int:len>', methods=['GET'])
def list_keys_by_len(len):
    list = redis.keys('?'*len)
    result = []
    for one in list:
        result.append(one.decode())
    return vo.multiple(result)

@app.route(url+'/key/<string:key>', methods=['GET'])
def get_key(key):
    re = redis.type(key)
    if re == b'string':
        result = redis.get(key)
        if result != None:
            return vo.single(result.decode())
        else:
            return vo.fail(404)
    else:
        return vo.fail(405)


@app.route(url+'/show_code', methods=['GET'])
def show_code():
    list = {
        '404': "资源找不到",
        '405': "键类型错误",
        '406': "参数缺失",
        '407':"redis连接未初始化"
    }
    return vo.multiple(list)

#  TODO  如何处理这个redis连接问题
@app.route(url+'/init_redis', methods=['POST'])
def init_redis():
    list = ['host', 'port', 'password', 'db']
    if not request.json :
        return vo.fail(406)
    for one in list:
        if not one in request.json:
            return vo.fail(406)
    global redis 
    redis = RedisConfig(request.json['host'], request.json['port'], request.json['password'], request.json['db']).getConnection()
    print('初始化 ', redis)
    return vo.success()

