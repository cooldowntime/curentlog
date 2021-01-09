#!/usr/bin/python3
# -*- coding:utf-8 -*-

from fastapi import FastAPI

from current_log.current_log_router import log_router
from current_log.current_log_service import run_app

app = FastAPI()

app.include_router(log_router)

if __name__ == '__main__':
    # uvicorn.run(app='main:app', host="0.0.0.0", port=8080, reload=False, debug=True)
    run_app(app_name='junior_test_local', app_host='')
    # run_app(system_name='junior_test_pass', host='juniorauto-testcenter.paas.cmbchina.cn')
