# -*- coding:utf-8 -*-
import win32serviceutil
import win32service
import win32event
from flask import Flask
from flask import request
import sys
import os
import requests
import shutil
import re
import time
from os import environ
# 设置编码
# reload(sys)
sys.setdefaultencoding('utf-8')


# windows服务中显示的名字
class WechatService(win32serviceutil.ServiceFramework):
    _svc_name_ = 'xf_rest'  # 可以根据自己喜好修改
    _svc_display_name_ = 'xf_rest'  # 可以根据自己喜好修改
    _svc_description_ = 'xf_rest'  # 可以根据自己喜好修改

    def __init__(self,args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.run = True

    def SvcDoRun(self):
         
        ##############################################################
        #########flask路由设置区，自定义功能也放在这里################
        ##############################################################
        from front import app

        #使用flask自带的web服务器
        ##############################################################
        #############自定义功能区结束#################################
        ##############################################################
        @app.route('/')
        def hello():
            """Renders a sample page."""
            return "Hello World!"

        HOST = environ.get('SERVER_HOST', '0.0.0.0')
        try:
            PORT = app.config["PORT"]
            # PORT = int(environ.get('SERVER_PORT', '5556'))
        except ValueError:
            PORT = 5555

        # 保存服务端口，后续定时任务要用到
        app.server_port = PORT

        # gevent异步WEB服务---------------------------------------------------
        from gevent import monkey, pywsgi
        monkey.patch_all()

        server = pywsgi.WSGIServer((HOST, PORT), app)
        server.serve_forever()

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)
        self.run = False
        # 00000


if __name__ == '__main__':
    import sys
    import servicemanager

    if len(sys.argv) == 1:
        try:
            evtsrc_dll = os.path.abspath(servicemanager.__file__)
            servicemanager.PrepareToHostSingle(WechatService)  # 如果修改过名字，名字要统一
            servicemanager.Initialize('WechatService',evtsrc_dll)  # 如果修改过名字，名字要统一
            servicemanager.StartServiceCtrlDispatcher()
        except win32service.error as details:
            import winerror
            if details == winerror.ERROR_FAILED_SERVICE_CONTROLLER_CONNECT:
                win32serviceutil.usage()
    else:
        win32serviceutil.HandleCommandLine(WechatService)  # 如果修改过名字，名字要统一
