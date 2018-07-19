from app import app
from flask import request, redirect
from base.ResultVO import ResultVO as vo
from base.RedisConfig import RedisConfig
import datetime

from .Config import Config
from .Line import Line

url = '/redis/api/v1.0'
# redis = RedisConfig('127.0.0.1', 6666, None, 0).getConnection()
redis = None
mainConfig = Config(url, redis)

"""
    author kuangcp
    展示按键数据的接口
"""
# url_for方法能得到相对路径
@app.before_request
def check():
    global redis
    path = request.path
    print('listen : ', path)
    # 如果路径中包含以下, 就全部忽略校验
    ignore = ['init_redis', 'show_code', '/static/']
    isIgnore = False
    for one in ignore:
        if one in path:
            isIgnore = True
            break
        if path == '/':
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


def period_key(length, offset):
    """获取时间数组"""
    days = []
    for i in range(offset, length+offset):
        now_time = datetime.datetime.now()
        yes_time = now_time + datetime.timedelta(i*-1)
        new_time = yes_time.strftime('%Y-%m-%d')
        days.append(new_time)
    return days

def period_key_with_total(length, offset):
    """获取时间数组,以及对应的按键总数"""
    days = period_key(length, offset)
    result = []
    for day in days:
        total = redis.get('all-'+day)
        if total is not None:
            result.append(day+'#'+total.decode())
        else:
            result.append(day+'#0')
    return result


def most_key(length, offset, top):
    """获取按键最多的键的code"""
    days = period_key(length, offset)
    # 将每天前五, 敲击次数最多的键的并集
    result = []
    for day in days:
        keyList = []
        for key,_ in redis.zrevrange(day, 0, top, True):
            # print(day, key, value)
            key = key.decode()
            keyList.append(key)
        result = list(set(keyList).union(set(result)))
    # print(result)
    return result,days

def most_key_name(result):
    """"获取最多键, 及其名字"""
    keys = []
    for key in result:
        key_name = redis.hget('key_map', key).decode()
        keys.append(key_name)
    return keys

@app.route(url + '/recent_day/<int:length>/<int:offset>', methods=['GET'])
def get_recent_day(length=7, offset=0):
    days = period_key_with_total(length, offset)
    return vo.multiple(days)

# TODO 校验三个参数的合法性  
@app.route(url + '/most_key/<int:length>/<int:offset>/<int:top>', methods=['GET'])
def get_most_key(length=7, offset=0, top=5):
    result = most_key(length, offset, top)[0]
    return vo.multiple(most_key_name(result))

@app.route(url + '/most_key_with_num/<int:length>/<int:offset>/<int:top>', methods=['GET'])
def get_most_key_with_num(length=7, offset=0, top=5):
    """组装前端需要的数据结构"""
    result,days = most_key(length, offset, top)
    lines = []
    for key in result:
        data = []
        for day in days:
            score = redis.zscore(day, key)
            if score is None:
                data.append(0)
            else:
                data.append(int(score))
        line = Line(redis.hget('key_map',key).decode(), data).to_json_self()
        lines.append(line)
    return vo.multiple(lines)
