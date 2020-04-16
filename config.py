import logging
import os  
import time
import pymysql

from urllib.parse import quote as urlquote

# 应用根目录
# basedir = os.path.abspath(os.path.dirname(__file__))

# 数据库
# 参考: http://www.pythondoc.com/flask-sqlalchemy/config.html
# 参考: https://blog.csdn.net/ennismar/article/details/59518653


SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:hujin66.@sponge_db_ip:3306/sponge?charset=utf8'
# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:hujin666..@localhost:3306/sponge?charset=utf8'
PORT = 8080
# redis信息
REDIS_CONF = {
    "host": 'localhost',
    "port": 6379,
    "db": 0
}
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_POOL_SIZE = 5
SQLALCHEMY_POOL_RECYCLE = 3600

# TOKEN鉴权使用的安全因子
SECRET_KEY = 'lazy dog'

# 静态文件目录,文件落地目录
STATIC_FOLDER = './static'
# 缓存类型及默认超时时间
CACHE_TYPE ='simple'
CACHE_DEFAULT_TIMEOUT = 60


#  账号加解密
AES_KEY = "12345678"
#  初始密码
INIT_PASSWORD = "xd12345678"
#  token有效期 秒
CLIENT_TOKEN_EXP = 3600

