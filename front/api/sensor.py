from front.logger import app
from copy import deepcopy
from front.libs.dst import my_json
from flask import request, g
from front.libs.auth import verify_account
from front.models.sensor_data import SensorDatum
from front.models.sensors import Sensor
from front.libs.default_data import address as default_address
import datetime
from front.libs import auth


@app.route('/sponge/data/sensor', methods=["GET"])
# @auth.auth_required
def sensor_data():
    """
    传感器数据接口
    :return: dst.my_json字典
    """
    result = deepcopy(my_json)  # 存储给用户的提示信息msg以及给前端的状态码
    args = dict()
    args["start"] = request.args.get("start", "2019-06-22") + " 00:00:00"  # 开始时间 默认是2019-06-22
    args["end"] = request.args.get("end", str(datetime.date.today() + datetime.timedelta(days=1))) + " 00:00:00"
    # 结束时间 默认是今天
    args["interval"] = request.args.get("interval", 60)  # 时间间隔 默认60s
    args["address"] = request.args.get("address", default_address)  # 地点
    args["sensor_id"] = request.args.get("sensor_id", None)  # 数据类型
    success, result["message"] = SensorDatum.sensor_args_check(args)  # 检查参数值是否合法
    if not success and args["sensor_id"]:
        result["status"] = 0
        return result
    success, result["message"], result["data"] = SensorDatum.get_data(args)
    result["status"] = 1 if success else 0
    return result


@app.route('/sponge/sensors/list', methods=["GET"])
# @auth.auth_required
def sensors_list():
    """
    传感器列表数据接口
    :return: dst.my_json字典
    """
    result = deepcopy(my_json)  # 存储给用户的提示信息msg以及给前端的状态码
    result["data"] = Sensor.get_all_sensors()
    return result
