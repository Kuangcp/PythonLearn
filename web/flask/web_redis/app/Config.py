# 公共配置类

class Config:
    def __init__(self, url, redis):
        self.url = url 
        self.redis = redis
    
    def getUrl(self):
        return self.url 

    def getRedis(self):
        return self.redis
    
    def setRedis(self, redis):
        self.redis = redis