import logging
from logging.handlers import RotatingFileHandler
import os
import time
from flask_api import status
from front import app
import functools
import traceback
# 中文编码
import importlib, sys
importlib.reload(sys)


def getExePath():
    sap = '/'
    if sys.argv[0].find(sap) == -1:
        sap = '\\'
    indx = sys.argv[0].rfind(sap)
    path = sys.argv[0][:indx] + sap
    return path


LOG_FORMAT = '%(asctime)s %(levelname)s: %(message)s\r\n'

# 访问日志路径及日志级别
LOG_PATH = getExePath()+'Logs/info/%s.log' % (time.strftime('%Y%m%d'))
# LOG_PATH = 'Logs/%s.log' %(time.strftime('%Y%m%d'))
LOG_LEVEL = logging.INFO

logdir, _ = os.path.split(LOG_PATH)

# 错误日志路径及日志级别
ERROR_LOG_PATH = getExePath()+'Logs/error/%s.log' % (time.strftime('%Y%m%d'))
error_logdir, _ = os.path.split(ERROR_LOG_PATH)
ERROR_LOG_LEVEL = logging.ERROR


# 创建日志目录
if not os.path.exists(logdir):
    os.makedirs(logdir)
if not os.path.exists(error_logdir):
    os.makedirs(error_logdir)

file_handler = RotatingFileHandler(LOG_PATH, 'a', 1 * 1024 * 1024, 10)
file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

error_handler = RotatingFileHandler(ERROR_LOG_PATH, 'a', 1 * 1024 * 1024, 10)
# error_handler.setFormatter(logging.Formatter(LOG_FORMAT))


app.logger.addHandler(file_handler)
app.logger.setLevel(LOG_LEVEL)
app.logger.addHandler(error_handler)
app.logger.setLevel(ERROR_LOG_LEVEL)


@app.errorhandler(400)
def errorhandler_400(error):
    app.logger.info(error.description.encode("utf-8"))
    return error.description, status.HTTP_400_BAD_REQUEST


@app.errorhandler(404)
def errorhandler_404(error):
    app.logger.info(error.description.encode("utf-8"))
    return error.description, status.HTTP_404_NOT_FOUND


@app.errorhandler(Exception)
def framework_error(error):
    app.logger.error(str(error), exc_info=True)
    return str(error), status.HTTP_500_INTERNAL_SERVER_ERROR


# def create_logger():
#     if not os.path.exists(error_logdir):
#         os.makedirs(error_logdir)
#     logger = logging.getLogger(ERROR_LOG_PATH)
#     logger.setLevel(logging.ERROR)
#     fh = logging.FileHandler(ERROR_LOG_PATH)
#     fmt = "\n[%(asctime)s-%(name)s-%(levelname)s]: %(message)s"
#     formatter = logging.Formatter(fmt)
#     fh.setFormatter(formatter)
#     logger.addHandler(fh)
#     return logger
#
#
# def error_log(fn):
#     @functools.wraps(fn)
#     def wrapper(*args, **kwargs):
#
#         logger = create_logger()
#         try:
#             res = fn(*args, **kwargs)
#         except Exception as e:
#             logger.exception("[Error in {}] msg: {}".format(__name__, str(e)))
#         return res
#     return wrapper
