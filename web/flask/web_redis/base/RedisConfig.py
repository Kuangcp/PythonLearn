import redis

class RedisConfig:
    def __init__(self, host, port, password, db):
        self.host = host
        self.port = port
        self.password = password
        self.db = db

    def getConnection(self):
        return redis.Redis(self.host, self.port, self.db, self.password)
   