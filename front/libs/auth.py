# coding:utf-8
from functools import wraps
from flask import request, abort
from flask_httpauth import HTTPBasicAuth
from front import db
# from front import db, rdb, app
from front.models.user import User
from front import app, cache
from flask import g
from sqlalchemy import and_
auth = HTTPBasicAuth()


def verify_account(username, password):
    user = db.session.query(User).filter_by(username=username)
    g.user_query = user  # 保存这个查询
    user = user.first()
    if not user:
        return False, "ヾ(×× ) ﾂ闪瞎眼 此用户名未注册", 0
    if not user.verify_password(password):
        return False, "ヽ(o_ _)o摔倒 密码错误", 2
    g.user = user  # 保存这个查询到g.user
    return True, "ヾ(o◕∀◕)ﾉヾ兴奋 登录成功", 1


def get_token():
    if 'Authorization' in request.headers:
        try:
            authorization = request.headers['Authorization']
            token_type, token = authorization.split(None, 1)
        except ValueError:
            # The Authorization header is either empty or has no token
            token_type = token = None
    else:
        token_type = token = None

    return token_type, token


def validate_token(token):
    # 验证token的有效性
    data = User.verify_parse_token(token)
    if not data:
        app.logger.error("token:[%s]错误" % token)
        return False
    # 验证token是否存在缓存中
    user_dict = cache.get(data['id'])
    if not user_dict:
        app.logger.error("用户登录token[%s]缓存中不存在" % token)
        return False

    user = db.session.query(User).filter_by(id=data['id']).first()
    if user is None:
        return False
    g.user = user
    g.token = token
    return True


def clear_token(token):
    cache.delete(token)
    app.logger.info("[清除token] %s" % token)


def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token_type, token = get_token()
        if request.method != 'OPTIONS':
            params = request.get_json()
            app.logger.info("[接口访问]上传参数：%s" % params)
            if not (token_type and token):
                return abort(400, 'The user basic info need.')
            else:
                if token_type is None or token_type.lower() != 'basic':
                    return abort(401, 'The token type must be basic.')
                if token is None:
                    return abort(401, 'The token not exist.')
                if not validate_token(token):
                    return abort(401, 'The token error.')
        return f(*args, **kwargs)
    return decorated


def build_result(*_args, **_kwargs):
    """构造返回结果"""
    def build_result_wrap(func, *args, **kwargs):
        @wraps(func)
        def wrap_fun(*args, **kwargs):
            ret = func(*args, **kwargs)
            if len(ret) == 2:
                ok, message = ret
                data = None
            else:
                ok, message, data = ret

            result = {}
            if data is None:
                data = []
            result["ok"] = ok
            result["message"] = message
            result["data"] = data
            if _kwargs.get("ret_json",""):
                return result
            return result
        return wrap_fun
    return build_result_wrap


def return_Responed(ok, message, data=None):
    if data is None:
        data = {}
    return ok, message, data