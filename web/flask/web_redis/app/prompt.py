from app import app
from flask import request, redirect
from base.ResultVO import ResultVO as vo
from base.RedisConfig import RedisConfig

from .Config import Config

url = '/redis/api/v1.0'
# redis = RedisConfig('127.0.0.1', 6666, None, 0).getConnection()
redis = None
mainConfig = Config(url, redis)


# url_for方法能得到相对路径
@app.before_request
def check():
    global redis
    path = request.path
    # 如果路径中包含以下, 就全部忽略校验
    ignore = ['init_redis', 'show_code', 'html', 'css', 'js', 'jpg', '/static/']
    isIgnore = False
    for one in ignore:
        if one in path:
            isIgnore = True
            break
    if redis is None and not isIgnore:
        return vo.fail(407)
    else:
        redirect(path)

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
        print('Failed to connect', e)
        redis = None
        mainConfig.setRedis(None)
        return vo.fail(408)
    print('Successfully initialized Redis ', redis)
    mainConfig.setRedis(redis)
    return vo.success()
