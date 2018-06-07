from base.RedisConfig import RedisConfig
from base.ResultVO import ResultVO as vo

from flask import *
from flask_cors import CORS

redis = None
app = Flask(__name__, static_folder='./static')
CORS(app, supports_credentials=True)

# 构造应用基础路径
url = '/redis/api/v1.0'


# url_for方法能得到相对路径
@app.before_request
def check():
    global redis
    path = request.path
    # 如果路径中包含以下, 就全部忽略校验
    ignore = ['init_redis', 'show_code', 'html', 'css', 'js', 'jpg', '/static/']
    isIgnore = False

    # if path == '/static/':
    #     print(path + 'index.html')
    #     redirect('/static/index.html')
    #     return
    for one in ignore:
        if one in path:
            isIgnore = True
            break
    if redis is None and not isIgnore:
        return vo.fail(407)
    else:
        redirect(path)


@app.route(url + '/keys', methods=['GET'])
def list_keys():
    """ 列出 所有键"""
    all_key = redis.keys()
    result = []
    for one in all_key:
        result.append(one.decode())
    return vo.multiple(result)


@app.route(url + '/keys/<int:length>', methods=['GET'])
def list_keys_by_len(length):
    """列出所有, 按键的长度"""
    key_list = redis.keys('?' * length)
    result = []
    for one in key_list:
        result.append(one.decode())
    return vo.multiple(result)


@app.route(url + '/key/<string:key>', methods=['GET'])
def key_get(key):
    re = redis.type(key)
    if re == b'string':
        result = redis.get(key)
        if result is not None:
            return vo.single(result.decode())
        else:
            return vo.fail(404)
    else:
        return vo.fail(405)


@app.route(url + '/key', methods=['POST'])
def key_set():
    redis_config = ['key', 'value']
    if not request.json:
        return vo.fail(406)
    for one in redis_config:
        if one not in request.json:
            return vo.fail(406)
    redis.set(request.json['key'], request.json['value'])


@app.route(url + '/show_code', methods=['GET'])
def show_code():
    result_code = {
        '404': "资源找不到"
        , '405': "键类型错误"
        , '406': "参数缺失"
        , '407': "redis连接未初始化"
        , '408': "redis连接失败"
    }
    return vo.multiple(result_code)


#  TODO  如何处理这个redis连接问题
@app.route(url + '/init_redis', methods=['POST'])
def init_redis():
    config_list = ['host', 'port', 'password', 'db']
    if not request.json:
        return vo.fail(406)
    for one in config_list:
        if one not in request.json:
            return vo.fail(406)
    global redis
    redis = RedisConfig(request.json['host'], request.json['port'], request.json['password'],
                        request.json['db']).getConnection()
    try:
        redis.ping()
    except Exception as e:
        print('连接失败', e)
        redis = None
        return vo.fail(408)
    print('成功初始化Redis ', redis)
    return vo.success()
