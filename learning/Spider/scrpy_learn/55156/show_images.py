import redis

def getconn():
    return redis.Redis(host='localhost', port=6379, db=0)

conn = getconn()
list = conn.smembers('images')
fileName = 1
count = 1
targetFile = open('result/'+str(fileName)+".md", "w+")
for line in list:
    count += 1
    if type(line) == bytes:
        line = line.decode('utf-8')
        targetFile.write('![0]('+line+')\n')
    if count % 101 == 0 :
        fileName += 1
        targetFile.close()
        targetFile = open('result/'+str(fileName)+".md", "w+")

