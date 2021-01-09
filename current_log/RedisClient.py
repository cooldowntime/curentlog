# -*- coding: utf-8 -*-

import redis

REDIS_CONFIG = {
    'host': '',
    'port': 6379,
    'db': 15,
    'decode_responses': True,
    'socket_connect_timeout': 1
}

class RedisClient():

    def __init__(self):
        self.connection_pool = redis.ConnectionPool(host=REDIS_CONFIG['host'], port=REDIS_CONFIG['port'],
                                                    db=REDIS_CONFIG['db'], decode_responses=REDIS_CONFIG['decode_responses'],
                                                    socket_connect_timeout=REDIS_CONFIG['socket_connect_timeout'])
        self.connection_client = redis.StrictRedis(connection_pool=self.connection_pool)

    def rpush(self, key, jsonStr):
        """
        添加字符串元素到对应list尾部
        :param key: redis数据库list的名字
        :param jsonStr: 存入list的json字串
        :return:
        """
        r = self.connection_client
        r.rpush(key, jsonStr)

    def lpop(self, key):
        """
        从list中返回并删除第一个元素
        :param key: redis数据库list的名字
        :return: list中的第一个元素
        """
        r = self.connection_client
        data = r.lpop(key)
        return data

    def get(self, key):
        r = self.connection_client
        data = r.get(key)
        return data

    def set(self, key, value):
        r = self.connection_client
        data = r.set(key, value)
        return data

if __name__ == '__main__':
    redis_client = RedisClient()
    redis_client.set("aaa", "bbb")
    aaa = redis_client.get("aaa")
    print(aaa)
