# -*- coding: utf-8 -*-
# @Time : 2020/12/28 16:53
# @Author : chendi
# @Email : chendi1994@cmbchina.com
# @File : current_log_router.py
# @Project : current_log
import asyncio
import traceback
from datetime import datetime
from typing import List

from fastapi import APIRouter, Request, WebSocket
from starlette.responses import HTMLResponse

from current_log.RedisClient import RedisClient

log_router = APIRouter()

html = """
<!DOCTYPE html>
<html lang="zh-cn">
    <head>
        <meta charset="UTF-8">
        <title>实时日志</title>
    </head>
    <body>
        <h2>实时日志</h2>
        <div id="log"></div>
        <script>
            var ws = new WebSocket("ws://{host}/log_connect/{user}");
            var heartCheck = {{
                timeout: 60000,//60ms
                timeoutObj: null,
                reset: function(){{
                    clearTimeout(this.timeoutObj);
            　　　　 this.start();
                }},
                start: function(){{
                    this.timeoutObj = setTimeout(function(){{
                        ws.send("HeartBeat");
                    }}, this.timeout)
                }}
            }}
            ws.onopen = () => {{
                console.log("websocket连接")
                heartCheck.start();
            }}
            ws.onmessage = function(event) {{
                heartCheck.start();
                var data = event.data
                if (data !== 'pong') {{
                    var log_div = document.getElementById('log')
                    log_div.innerHTML = log_div.innerHTML + data + '<br/>'
                }}
            }}
            ws.onclose = function () {{
                console.log("websocket断开连接")
            }}
            window.onbeforeunload = () => {{
                ws.close()
            }}
        </script>
    </body>
</html>"""

redis_client = RedisClient()


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def broadcast(self, system_name):
        while True:
            message = redis_client.lpop(system_name)
            if message:
                # await asyncio.gather(
                #     *[ws.send_text(message) for ws in self.active_connections],
                #     return_exceptions=False,
                # )
                for ws in self.active_connections:
                    try:
                        await ws.send_text(message)
                    except:
                        pass
            await asyncio.sleep(0.2)

    def start_broadcast(self, system_name):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        asyncio.get_event_loop().run_until_complete(manager.broadcast(system_name))
        # asyncio.get_event_loop().run_forever()


manager = ConnectionManager()


@log_router.get(path='/logs')
def get_log(request: Request):
    try:
        run_host = str(request.url.netloc)
        user = datetime.now().strftime('%f')
        user_html = html
        user_html = user_html.format(host=run_host, user=user)
        return HTMLResponse(user_html)
    except:
        return {"error": traceback.format_exc()}


@log_router.websocket(path="/log_connect/{user}")
async def broadcast_log_redis(ws: WebSocket, user: str):
    await ws.accept()
    manager.active_connections.append(ws)
    try:
        while True:
            await ws.receive_text()
            await ws.send_text("pong")
    except:
        pass
    finally:
        manager.active_connections.remove(ws)


@log_router.get(path="/start_generate_log/{system_name}")
def start_generate_log(system_name: str):
    import threading
    threading.Thread(target=manager.start_broadcast, args=(system_name,)).start()
    return {"message": "success"}


@log_router.get(path='/')
def test():
    print("测试")
    return {"message": "aaaa"}
