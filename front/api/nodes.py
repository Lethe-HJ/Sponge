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
# @auth.auth_required
def node_list():
    """
    基站列表数据接口
    return: dst.my_json字典
    """
    result = deepcopy(my_json)  # 存储给用户的提示信息msg以及给前端的状态码
    success, result["message"], result["data"] = Node.get_all_nodes()
    result["status"] = 1 if success else 0
    return result


@app.route('/sponge/nodes/eidt', methods=["PUT"])
def node_eidt(): 
    """
    基站数据编辑接口
    return: dst.my_json字典
    """
    result = deepcopy(my_json)  # 存储给用户的提示信息msg以及给前端的状态码
    args = dict()
    nid = request.args.get("nid", None)
    args["address"] = request.args.get("address", None)
    args["location"] = request.args.get("location", None)
    args["status"] = request.args.get("status", None)
    args["secret_key"] = request.args.get("secret_key", None)
    success, msg = Node.node_eidt_args_check(nid, args)  # 检查参数
    if not success:  # 参数不符合预期
        result["status"], result["message"] = 0, msg
        return result
    success, result["message"] = Node.edit_node(nid, args)
    result["status"] = 1 if success else 0
    return result

