import asyncio
import time
from datetime import datetime

import websockets

from current_log.RedisClient import RedisClient

system_name = 'junior_test_local'
CLIENTS = set()
redis_client = RedisClient()


async def broadcast():
    while True:
        message = redis_client.lpop(system_name)
        if message:
            await asyncio.gather(
                *[ws.send(message) for ws in CLIENTS],
                return_exceptions=False,
            )
        await asyncio.sleep(0.2)


asyncio.get_event_loop().create_task(broadcast())


async def handler(websocket: websockets.server.WebSocketServerProtocol, path: str):
    CLIENTS.add(websocket)
    try:
        async for msg in websocket:
            pass
    except:
        pass
    finally:
        CLIENTS.remove(websocket)


start_server = websockets.serve(handler, host="localhost", port=5678)
def put_redis():
    while True:
        data = datetime.now().strftime('%f')
        redis_client.rpush(system_name, data)
        time.sleep(1)
import threading
threading.Thread(target=put_redis).start()
print('aaa')
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
print('bbb')