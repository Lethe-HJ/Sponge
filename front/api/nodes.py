from front.logger import app
from copy import deepcopy
from front.libs.dst import my_json
from flask import request, g
from front.libs.auth import verify_account
from front.models.nodes import Node
from front.libs.default_data import address as default_address
from datetime import datetime
from front.libs import auth


@app.route('/sponge/nodes/list', methods=["GET"])
@auth.auth_required
def node_list():
    """
    基站列表数据接口
    :return: dst.my_json字典
    """
    result = deepcopy(my_json)  # 存储给用户的提示信息msg以及给前端的状态码
    success, result["message"], result["data"] = Node.get_all_nodes()
    result["status"] = 1 if success else 0
    return result

