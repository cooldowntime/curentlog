# -*- coding: utf-8 -*-
# @Time : 2020/12/16 15:36
# @Author : chendi
# @Email : chendi1994@cmbchina.com
# @File : log_service.py
# @Project : Training
import re
import subprocess
import threading

from current_log.RedisClient import RedisClient

redis_client = RedisClient()


def record_stream_redis(stream, system_name):
    for line in iter(stream.readline, b''):
        line = line.decode("utf8").strip()
        line = re.sub('\033\[(.*?)m', '', line)  # 去掉日志颜色信息，以后前端有时间优化
        if len(line) > 0:
            redis_client.rpush(system_name, line)


def run_app(app_name, app_host):
    if ":" in app_host:
        ip, port = app_host.split(":")
    else:
        port = 8080
    cmd = f'uvicorn main:app --host="0.0.0.0" --port {str(port)} --reload'
    process = subprocess.Popen(cmd,
                               shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=0)
    threading.Thread(target=record_stream_redis, args=(process.stderr, app_name)).start()
    threading.Thread(target=record_stream_redis, args=(process.stdout, app_name)).start()
    generate_log(app_host, app_name)


def generate_log(app_host, app_name):
    import requests
    res = requests.get(url=f"http://{app_host}/start_generate_log/{app_name}")
    assert res.json()['message'] == 'success'


if __name__ == '__main__':
    generate_log('192.168.8.179:8080', 'junior_test_local')
