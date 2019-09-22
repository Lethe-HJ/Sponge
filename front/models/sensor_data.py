# coding: utf-8
from front.models import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, exc
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship
from front import session
from front.models.sensor_type import SensorType
from front.libs.reg import date_reg
import random
import string
import re


class SensorDatum(Base):
    __tablename__ = 'sensor_data'

    data_id = Column(String(255), primary_key=True)
    sid = Column(Integer, nullable=False)
    datetime = Column(DateTime, nullable=False, server_default=FetchedValue())
    value = Column(String(255))
    type = Column(ForeignKey('sensor_type.id'), nullable=False, index=True)

    sensor_type = relationship('SensorType', primaryjoin='SensorDatum.type == SensorType.id', backref='sensor_data')

    @staticmethod
    def sensor_args_check(args):
        # 检查start字段的格式
        start = args["start"]
        reg_date = re.compile(date_reg)
        result = re.match(reg_date, start)
        if not result:
            return False, "start值格式错误"

        # 检查end字段的格式
        end = args["end"]
        result = re.match(reg_date, end)
        if not result:
            return False, "end值格式错误"

        # 检查interval字段的值 格式正整数
        if not re.match(r"^[1-9]\d*$", str(args["interval"])):
            return False, "start值格式错误"

        # args["address"]
        # 检查type的字段的值是否存在在sensor_type表中
        return True, ""

    @staticmethod
    def get_data(args):
        type_exist = session.query(SensorType.id).filter_by(id=args["type"]).first()
        if type_exist:
            type_id = type_exist[0]
        else:
            return False, "无此传感器类型", []
        id_data = session.query(SensorDatum.value, SensorDatum.datetime).filter(SensorDatum.type == type_id)
        all_data = id_data.filter(SensorDatum.datetime.between(args["start"], args["end"])).all()
        return True, "数据查询成功", [{"value": i.value, "datetime": i.datetime} for i in all_data]
