# coding: utf-8
from front.models import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, exc
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship
from front import session
from front.models.sensor_type import SensorType
from front.models.sensors import Sensor
from front.libs.reg import date_reg
import random
import string
import re
import time


class SensorDatum():
    #__tablename__ = 'sensor_data_1'

    #data_id = Column(String(255), primary_key=True)
    # sid = Column(Integer, nullable=False)
    #datetime = Column(DateTime, nullable=False, server_default=FetchedValue())
    #value = Column(String(255))
    # type = Column(ForeignKey('sensor_type.id'), nullable=False, index=True)

    # sensor_type = relationship('SensorType', primaryjoin='SensorDatum.type == SensorType.id', backref='sensor_data')

    @staticmethod
    def sensor_args_check(args):
        # 检查start字段的格式
        start = args["start"]
        result = re.match(r"^[1-9]\d*$", start)
        if not result:
            return False, "start值格式错误"

        # 检查end字段的格式
        end = args["end"]
        result = re.match(r"^[1-9]\d*$", end)
        if not result:
            return False, "end值格式错误"

        # 检查interval字段的值 格式正整数
        if "interval" in args.keys() and args["interval"] not in ["1", "2", "3"]:
            return False, "interval值不在可选列表中"

        # args["address"]
        # 检查type的字段的值是否存在在sensor_type表中
        return True, ""


    @staticmethod
    def get_avg_data(args):
        sensor_exist = session.query(Sensor.sid).filter_by(sid=args["sensor_id"]).first()
        if not sensor_exist:
            return False, "", []
        table_name = 'sensor_data_%s_avg' % str(args["sensor_id"])
        start = int(args["start"] + "0000")
        end = int(args["end"] + "0000")
        sql_0 = """
            (SELECT `value`, `time`
            FROM {0}
            WHERE time <= {1}
            ORDER BY `time` DESC
            LIMIT 1)
        UNION ALL
            (SELECT `value`, `time`
            FROM {0}
            WHERE (time BETWEEN {1} AND {2}) AND accuracy={3})
        UNION ALL
            (SELECT `value`, `time`
            FROM {0}
            WHERE time >= {2}
            ORDER BY `time`
            LIMIT 1);
        """.format(table_name, start, end, args["interval"])
        all_data = session.execute(sql_0).fetchall()
        return True, "数据查询成功", [{"value": i.value, "datetime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(i.time/10000))} for i in all_data]


    @staticmethod
    def get_detail_data(args):
        sensor_exist = session.query(Sensor.sid).filter_by(sid=args["sensor_id"]).first()
        if not sensor_exist:
            return False, "无此传感器", []
        table_name = 'sensor_data_%s_avg' % str(args["sensor_id"])
        start = int(args["start"] + "0000")
        end = int(args["end"] + "0000")
        sql_2 = """
            SELECT `value`, `time`
            FROM {0}
            WHERE time BETWEEN {1} AND {2}
            ORDER BY `time` DESC;
        """.format(table_name, start, end)
        all_data = session.execute(sql_2).fetchall()
        return True, "数据查询成功", [{"value": i.value, "datetime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(i.time/10000))} for i in all_data]

