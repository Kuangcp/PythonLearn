import redis

def getconn():
    return redis.Redis(host='localhost', port=6379, db=0)

conn = getconn()
list = conn.smembers('images')
with open('show.md','w+') as show:
    
    for line in list:
        #print('- ',line)
        if type(line) == bytes:
            line = line.decode('utf-8')
        show.write('![12]('+line+')\n')
