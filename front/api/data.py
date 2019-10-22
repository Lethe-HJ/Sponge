from front.logger import app
from copy import deepcopy
from front.libs.dst import my_json
from flask import request, g
from front.libs.auth import verify_account


@app.route('/sponge/data', methods=["GET"])
def data():
    """
    数据获取接口
    :return: dst.my_json字典
    """
    result = deepcopy(my_json)  # 存储给用户的提示信息msg以及给前端的状态码
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    success, result["message"], result["status"] = verify_account(username, password)  # 验证账户
    if success:
        token = g.user.generate_auth_token()
        g.user.save_token(g.user.ID, token)  # 保存token到缓存
        result["data"][0] = {
            "token": token,
            "user_id": g.user.ID,
            "username": username
        }
    return result


@app.route('/sponge/dashboard', methods=["GET"])
def dashboard():
    """
    仪表盘数据获取接口
    :return: dst.my_json字典
    """
    result = deepcopy(my_json)  # 存储给用户的提示信息msg以及给前端的状态码
    # 获取latest表中的当所有当前数据data = {"data": [{""}]}
    return result