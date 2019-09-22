from front.logger import app
from copy import deepcopy
from front.libs.dst import my_json
from front.libs import auth
from flask import request
from front.models.other.t_daily_record import TDailyRecord as TbDaily
# from front.logger import error_log


@app.route('/iims/dailies/data', methods=["GET"])
@auth.auth_required
def dailies_data():
    """
    个人日报数据接口d0
    :return: dst.my_json字典
    """
    result = deepcopy(my_json)  # 存储给用户的提示信息msg以及给前端的状态码
    detail = bool(request.args.get('detail', None))  # 前端传过来的的true与false是字符串 需转为bool
    start = request.args.get('start', None)
    end = request.args.get('end', None)
    page = request.args.get('page', None)  # 分页预留
    per_page = request.args.get('per_page', None)  # 分页预留
    result["data"] = TbDaily.his_all_daily(detail, start, end)
    result["message"] = "工作日报数据获取成功"
    return result


@app.route('/iims/dailies/query', methods=["GET"])
@auth.auth_required
def dailies_query():
    """
    个人日报查询接口d1
    :return: dst.my_json字典
    """
    result = deepcopy(my_json)  # 存储给用户的提示信息msg以及给前端的状态码
    detail = bool(request.args.get('detail', None))  # 前端传过来的的true与false是字符串 需转为bool
    query = request.args.get('query', None)
    page = request.args.get('page', None)  # 分页预留
    per_page = request.args.get('per_page', None)  # 分页预留
    result["data"] = TbDaily.query_daily(detail, query)
    result["message"] = "工作日报数据获取成功"
    return result


@app.route('/iims/dailies/add', methods=["POST"])
@auth.auth_required
def dailies_add():
    """
    日报新增提交接口d2
    :return: dst.my_json字典
    """
    result = deepcopy(my_json)  # 存储给用户的提示信息msg以及给前端的状态码
    args = {}
    try:
        args['WorkHours'] = request.json['work_hours']
        args['WorkMatters'] = request.json['work_matters']
        args['ProjectID'] = request.json['project_id']
        args['workintroId'] = request.json['workintro_id']
        args['WorkDate'] = request.json['work_date']
    except KeyError as e:
        result["message"] = e.args[0] + "字段不能为空"
        result["status"] = "0"
        return result
    work_matters = request.json.get('work_matters', None)  # remark字段可以为空
    args['WorkMatters'] = work_matters.encode('latin-1').decode('gbk')
    TbDaily.add_daily(**args)
    result["message"] = "添加工作日报成功"
    return result


@app.route('/iims/dailies/edit', methods=["PUT"])
@auth.auth_required
def dailies_edit():
    """
    日报编辑提交接口d5
    :return: dst.my_json字典
    """
    result = deepcopy(my_json)  # 存储给用户的提示信息msg以及给前端的状态码
    args = {}
    try:
        daily_id = request.json['daily_id']
        args['WorkHours'] = request.json['work_hours']
        args['WorkMatters'] = request.json['work_matters']
        args['ProjectID'] = request.json['project_id']
        args['workintroId'] = request.json['workintro_id']
        args['WorkDate'] = request.json['work_date']
    except KeyError as e:
        result["message"] = e.args[0] + "字段不能为空"
        result["status"] = "0"
        return result
    work_matters = request.json.get('work_matters', None)  # remark字段可以为空
    args['WorkMatters'] = work_matters.encode('latin-1').decode('gbk')
    success, result["message"] = TbDaily.edit_daily(daily_id, **args)
    result["status"] = 1 if success else 0
    return result


@app.route('/iims/dailies/edit/data', methods=["GET"])
@auth.auth_required
def dailies_edit_data():
    """
    当前日报信息接口d4
    :return: dst.my_json字典
    """
    result = deepcopy(my_json)  # 存储给用户的提示信息msg以及给前端的状态码
    result["data"] = {}

    try:
        daily_id = request.args["daily_id"]  # 日报id必须有
    except KeyError as e:
        result["message"] = e.args[0] + "字段不能为空"
        result["status"] = "0"
        return result

    # 查询当前工作日报的编辑信息
    success, result["message"], result["data"] = TbDaily.get_the_daily(daily_id)
    return result
