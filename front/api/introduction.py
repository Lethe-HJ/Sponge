from front.logger import app
from copy import deepcopy
from front.libs.dst import my_json
from front.libs.args import check_empty_args
from front.libs import auth
from flask import request
from front.models.other.t_work_introduction import TWorkIntroduction as TbIntros

# from front.logger import error_log
result = deepcopy(my_json)


@app.route('/iims/intros/data', methods=["GET"])
@auth.auth_required
def intros_data():
    """
    工作简介数据接口i1
    :return: dst.my_json字典
    """
    detail = bool(request.args.get('detail', None))  # 前端传过来的的true与false是字符串 需转为bool
    query = request.args.get('query', None)
    page = request.args.get('page', None)  # 分页预留
    per_page = request.args.get('per_page', None)  # 分页预留
    result["data"] = TbIntros.himself_intros(detail)
    result["message"] = "数据获取成功"
    result["status"] = 1
    return result


@app.route('/iims/intros/query', methods=["GET"])
@auth.auth_required
def intros_query():
    """
    工作简介查询接口i2
    :return: dst.my_json字典
    """
    detail = bool(request.args.get('detail', None))
    query = request.args.get('query', None)
    page = request.args.get('page', None)  # 分页预留
    per_page = request.args.get('per_page', None)  # 分页预留
    success, result["message"], result["data"] = TbIntros.query_daily(detail, query)
    result["status"] = 1 if success else 0
    return result


@app.route('/iims/intros/edit/data', methods=["GET"])
@auth.auth_required
def intros_edit_data():
    """
    当前工作简介信息接口i4
    :return: dst.my_json字典
    """
    result["data"] = {}
    args = {}
    try:
        args["intro_id"] = request.args["intro_id"]  # 日报id必须有
        check_empty_args(args)
    except KeyError as e:
        result["message"] = e.args[0] + "字段不能无或为空"
        result["status"] = "0"
        return result
    # 查询当前工作日报的编辑信息
    success, result["message"], result["data"] = TbIntros.get_the_intro(args["intro_id"])
    result["status"] = 1 if success else 0
    return result


@app.route('/iims/intros/add', methods=["POST"])
@auth.auth_required
def intros_add():
    """
    工作简介新增提交接口i3
    :return: dst.my_json字典
    """

    args = {}
    try:
        args["workaddress"] = request.json['work_address']
        args["workproperty"] = request.json['work_property_id']
        args["projectid"] = request.json['project_id']
        args["workintro"] = request.json['work_intro']
        check_empty_args(args)
    except KeyError as e:
        result["message"] = e.args[0] + "字段不能无或为空"
        result["status"] = "0"
        return result

    args["remarks"] = request.json.get('remarks', "")  # remark字段可以为空
    success, result["message"] = TbIntros.add_intro(**args)
    result["status"] = 1 if success else 0
    result["data"] = {}
    return result


@app.route('/iims/intros/edit', methods=["PUT"])
@auth.auth_required
def intros_edit():
    """
    工作简介编辑提交接口i5
    :return: dst.my_json字典
    """

    args = {}
    try:
        intro_id = request.json['intro_id']
        args["workaddress"] = request.json['work_address']
        args["workproperty"] = request.json['work_property_id']
        args["projectid"] = request.json['project_id']
        check_empty_args(args)
    except KeyError as e:
        result["message"] = e.args[0] + "字段不能无或为空"
        result["status"] = "0"
        return result
    args["workintro"] = request.json.get('work_intro', None)  # work_intro字段可以为空
    args["remarks"] = request.json.get('remarks', None)  # remark字段可以为空
    success, result["message"] = TbIntros.edit_intro(intro_id, **args)
    result["status"] = 1 if success else 0
    result["data"] = {}
    return result
