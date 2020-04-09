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
    return: dst.my_json字典
    """
    result = deepcopy(my_json)  # 存储给用户的提示信息msg以及给前端的状态码
    success, result["message"], result["data"] = Node.get_all_nodes()
    result["status"] = 1 if success else 0
    return result

@app.route('/sponge/nodes/get', methods=["GET"])
@auth.auth_required
def node_get():
    """
    基站列表数据接口
    return: dst.my_json字典
    """
    result = deepcopy(my_json)  # 存储给用户的提示信息msg以及给前端的状态码
    nid = request.args.get("nid", None)
    success, result["message"], result["data"] = Node.get_the_node(nid)
    result["status"] = 1 if success else 0
    return result


@app.route('/sponge/nodes/edit', methods=["PUT"])
@auth.auth_required
def node_edit(): 
    """
    基站数据编辑接口
    return: dst.my_json字典
    """
    result = deepcopy(my_json)  # 存储给用户的提示信息msg以及给前端的状态码
    args = dict()
    nid = request.json.get("nid", None)
    args["address"] = request.json.get("address", None)
    args["location"] = request.json.get("location", None)
    args["status"] = request.json.get("status", None)
    args["secret_key"] = request.json.get("secret_key", None)
    success, msg = Node().node_eidt_args_check(nid, args)  # 检查参数
    if not success:  # 参数不符合预期
        result["status"], result["message"] = 0, msg
        return result
    success, result["message"] = Node.edit_node(nid, args)
    result["status"] = 1 if success else 0
    return result


@app.route('/sponge/nodes/add', methods=["POST"])
@auth.auth_required
def node_add(): 
    """
    基站数据新增接口
    return: dst.my_json字典
    """
    result = deepcopy(my_json)  # 存储给用户的提示信息msg以及给前端的状态码
    args = dict()
    args["address"] = request.json.get("address", None)
    args["location"] = request.json.get("location", None)
    args["status"] = request.json.get("status", None)
    args["secret_key"] = request.json.get("secret_key", None)
    success, msg = Node().node_add_args_check(args)  # 检查参数
    if not success:  # 参数不符合预期
        result["status"], result["message"] = 0, msg
        return result
    success, result["message"] = Node.add_node(args)
    result["status"] = 1 if success else 0
    return result


@app.route('/sponge/nodes/delete', methods=["DELETE"])
@auth.auth_required
def node_del(): 
    """
    基站数据删除接口
    return: dst.my_json字典
    """
    result = deepcopy(my_json)  # 存储给用户的提示信息msg以及给前端的状态码
    args = dict()
    args["address"] = request.json.get("address", None)
    args["location"] = request.json.get("location", None)
    args["status"] = request.json.get("status", None)
    args["secret_key"] = request.json.get("secret_key", None)
    success, msg = Node().node_add_args_check(args)  # 检查参数
    if not success:  # 参数不符合预期
        result["status"], result["message"] = 0, msg
        return result
    success, result["message"] = Node.add_node(args)
    result["status"] = 1 if success else 0
    return result


