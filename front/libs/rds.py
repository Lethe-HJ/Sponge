# coding:utf-8

import redis
import pickle


class Redis:
    # @staticmethod
    rds = None

    # def __init__(self, app):
    #     self.app = app

    def connect(self, host='localhost', port=6379, db=0):
        self.rds = redis.StrictRedis(host, port, db)
        self.rds.ping()
        return self.rds

    # 将内存数据二进制通过序列号转为文本流，再存入redis
    # @staticmethod
    def set_data(self, key, data, ex=None):
        self.rds.set(pickle.dumps(key), pickle.dumps(data), ex)

    # 将文本流从redis中读取并反序列化，返回
    # @staticmethod
    def get_data(self, key):
        data = self.rds.get(pickle.dumps(key))
        if data is None:
            return None

        return pickle.loads(data)

    def del_data(self, key):
        self.rds.delete(pickle.dumps(key))

    def exists(self, keys):
        return self.rds.exists(pickle.dumps(keys))