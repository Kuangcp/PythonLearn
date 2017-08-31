import urllib.request as request
import redis
from time import sleep

# url = 'http://ovjs7rsrm.bkt.clouddn.com/china_area.jpg'  
# print("downloading with urllib")
# request.urlretrieve(url, "/home/kcp/test/a.jpg")
target_dir = "/home/kcp/Pictures/hunluan/siwa/"

def getconn(db):
    return redis.Redis(host='localhost', port=6379, db=db)
    
def down_image(url):
    print(url)
    try:
        request.urlretrieve(url, target_dir+""+url.split("/")[-1])
    except Exception:
        print("下载失败,稍后重试")

def download():
    origin = getconn(0)
    
    #  做差集运算
    origin.sdiffstore("nodown", "images", "downed")
    images = origin.smembers("nodown")
    count = 0
    
    for image in images:
        count += 1
        url = image.decode("utf-8")
        down_image(url)
        origin.srem("nodown", image)
        origin.sadd("downed", image)
        sleep(0.2)

def main():
    download()

main()