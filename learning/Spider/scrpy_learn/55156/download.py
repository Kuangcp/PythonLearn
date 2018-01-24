import urllib.request as request
import redis
from time import sleep
import sys

    
def down_image(target_dir, url):
    print(url)
    try:
        request.urlretrieve(url, target_dir+""+url.split("/")[-1])
    except Exception:
        print("下载失败,稍后重试,网络或目录不存在")

def download(host, port, db, target_dir, no_download, downloaded, password=None):
    if password == None:
        origin = redis.Redis(host=host, port=port, db=db)
    else:
        origin = redis.Redis(host=host, port=port, db=db, password=password)
    #  做差集运算
    origin.sdiffstore(no_download, "images", downloaded)
    images = origin.smembers(no_download)
    count = 0
    
    for image in images:
        count += 1
        url = image.decode("utf-8")
        down_image(target_dir, url)
        origin.srem(no_download, image)
        origin.sadd(downloaded, image)
        # origin.sremove()
        sleep(0.2)

def read_param():
    ''' 阅读参数 '''
    params = sys.argv
    # 没有参数就是本机
    if len(params) == 1:
        download("localhost", 6379, 2, "/home/kcp/Music/55156/siwa/", "nodown", "downed")
    elif params[1] == '80':
        download("120.25.203.47", 6380, 0, "/home/kcp/Pictures/hunluan/xinggan/","no_down2","downed2",password="myth")
    else:
        img_path = params[1]+"/img/"
        print("下载目录: "+img_path)
        download("localhost", 6379, 2, img_path, "nodown", "downed")
        

def main():
    read_param()
    
main()