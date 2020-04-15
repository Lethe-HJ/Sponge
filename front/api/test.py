
from front.logger import app
from copy import deepcopy
from front.libs.dst import my_json
from flask import request, g
from front.libs.auth import verify_account
from front.models.sensor_data import SensorDatum
from front.libs.default_data import address as default_address
from datetime import datetime


@app.route('/sponge/test/create_data', methods=["GET"])
def create_data():
    """
    随机数据生成接口
    :return: dst.my_json字典
    """
    args = dict()
    args["start"] = request.args.get("start", "2019-06-22")  # 开始时间 默认是2019-06-22
    args["end"] = request.args.get("end", str(datetime.now().date()))  # 结束时间 默认是今天
    args["interval"] = request.args.get("interval", 60)  # 时间间隔 默认60s
    args["address"] = request.args.get("address", default_address)  # 地点
    args["type"] = request.args.get("type", None)  # 数据类型
    return "hello world"

