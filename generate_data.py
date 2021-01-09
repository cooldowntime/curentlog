from datetime import datetime

from current_log.RedisClient import RedisClient
import time

system_name = 'junior_test_local'
redis_client = RedisClient()
def put_redis():
    while True:
        data = datetime.now().strftime('%f')
        print(data)
        redis_client.rpush(system_name, data)
        time.sleep(1)

def pop_redis():
    while True:
        data = redis_client.lpop(system_name)
        print(data)
pop_redis()