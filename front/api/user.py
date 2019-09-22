from front.logger import app
from copy import deepcopy
from front.libs.dst import my_json
from flask import request, g
from front.libs.auth import verify_account


@app.route('/sponge/user/login', methods=["POST"])
def login():
    """
    用户登录接口
    :return: dst.my_json字典
    """
    result = deepcopy(my_json)  # 存储给用户的提示信息msg以及给前端的状态码
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    success, result["message"], result["status"] = verify_account(username, password)  # 验证账户
    if success:
        token = g.user.generate_auth_token()
        g.user.save_token(g.user.id, token)  # 保存token到缓存
        result["data"][0] = {
            "token": token,
            "user_id": g.user.id,
            "username": username
        }
    return result


@app.route('/sponge/user/logout', methods=["GET"])
def logout():
    """
    用户登出接口
    """
    from front.libs.auth import clear_token
    clear_token(g.token)
