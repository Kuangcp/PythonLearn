from app import app
from flask import request
from base.ResultVO import ResultVO as vo

from .prompt import mainConfig

url = mainConfig.getUrl()
redis = mainConfig.getRedis()

@app.route(url + '/keys', methods=['GET'])
def list_keys():
    """ 列出 所有键"""
    redis = mainConfig.getRedis()
    all_key = redis.keys()
    result = []
    for one in all_key:
        result.append(one.decode())
    return vo.multiple(result)


@app.route(url + '/keys/<int:length>', methods=['GET'])
def list_keys_by_len(length):
    """列出所有, 按键的长度"""
    redis = mainConfig.getRedis()
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
        return vo.single(result.decode())
    elif re == b'none':
        return vo.fail(404)
    else:
        return vo.fail(405)


@app.route(url + '/key', methods=['POST'])
def key_set():
    redis_config = ['key', 'value']
    if not request.json:
        return vo.fail(406)
    for one in redis_config:
        if one not in request.json or request.json[one] == '':
            return vo.fail(406)
    redis.set(request.json['key'], request.json['value'])
    return vo.success()
