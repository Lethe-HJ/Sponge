#  coding:utf-8

# oracle中文编码问题
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
import sys

def getExePath():
    sap = '/'
    if sys.argv[0].find(sap) == -1:
        sap = '\\'
    indx = sys.argv[0].rfind(sap)
    path = sys.argv[0][:indx] + sap
    return path

from flask_api import FlaskAPI
from flask import Flask
app = FlaskAPI(__name__)

# Flask-API的渲染引擎
from flask_api.parsers import JSONParser
from flask_api import renderers
from front.utils.MyJSONRenderer import MyJSONRenderer

DEFAULT_RENDERERS = [
    'front.utils.MyJSONRenderer.MyJSONRenderer',
    'flask_api.renderers.BrowsableAPIRenderer',
]

# 预加载驱动
import pymysql
# 加载配置文件
# config_file = os.path.abspath('config.py')

# config_file = getExePath()+'config.py'
# app.config.from_pyfile(config_file)
config_file = "../config.py"
app.config.from_pyfile(config_file)
# 加载静态文件路径
static_folder = app.config['STATIC_FOLDER']
app = FlaskAPI(__name__,static_folder=static_folder)
app.config.from_pyfile(config_file)
app.config['DEFAULT_RENDERERS'] = DEFAULT_RENDERERS

# 数据库
from flask_sqlalchemy import SQLAlchemy

# 生产库
db = SQLAlchemy(app)
session = db.session
# 系统库
sysdb = SQLAlchemy(app)

from flask_cors import CORS

# 引入flask_restful
from flask_restful import Api
api = Api(app)

# 跨域处理
CORS(app, supports_credentials=True)

# 认证
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

# 认证

# from front import auth_handler
# 日志
from front import logger

# 缓存
from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()

from front.libs.rds import Redis
#  rds = None
#  rdb = Redis()
#  def init_redis(app):
#      global rds
#      rds = rdb.connect(**app.config["REDIS_CONF"])
#      if not rds:
#          #  连接化redis失败
#          raise Exception("connect redis fail")
#  init_redis(app)

# API业务
from front import api


# 访问日志
from front import accesslog
# 错误日志
