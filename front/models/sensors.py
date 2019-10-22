# coding: utf-8
from front.models import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, exc, Float
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship
from front import session
from front.models.sensor_type import SensorType
from front.models.nodes import Node
from front.libs.reg import date_reg
import random
import string
import re


class Sensor(Base):
    __tablename__ = 'sensors'

    sid = Column(Integer, primary_key=True)
    nid = Column(ForeignKey('nodes.nid'), nullable=False)
    name = Column(String(255), nullable=False)
    type = Column(ForeignKey('sensor_type.id'), nullable=False, index=True)
    allow_vary = Column(Float, nullable=False)
    latest_data = Column(String(255), nullable=False)
    data_updatetime = Column(Integer, nullable=False)
    node = relationship('Node', primaryjoin='Sensor.nid == Node.nid', backref='sensors')
    sensor_type = relationship('SensorType', primaryjoin='Sensor.type == SensorType.id', backref='sensors')

    @staticmethod
    def get_all_sensors():
        sql_1 = """
        SELECT `name`, s.nid AS `nid`, `sid`, `latest_data`, `data_updatetime`, `address`, `location`, `status`, `type_name` FROM `sensors` s
        LEFT JOIN
        (SELECT `nid`, `address`, `location`, `status` FROM `nodes`) n
        ON s.nid=n.nid
        LEFT JOIN
        (SELECT `id`, `name` AS `type_name` FROM `sensor_type`) t
        ON t.id=s.type;
        """
        datas = session.execute(sql_1).fetchall()
        return [{"name": data.name, "sid": data.sid, "nid": data.nid, "address": data.address, "location": data.location,
                 "status": data.status, "type": data.type_name, "data": data.latest_data, "update_time": data.data_updatetime} for data in datas]

    @staticmethod
    def sensors_vary_modify(sensor_id, value):
        the_sensor = session.query(Sensor.sid).filter_by(sid=sensor_id)
        if not the_sensor.first():
            return False, "无此传感器"
        if not re.match(r'^[1-9]\d*\.\d*|0\.\d*[1-9]\d*|0?\.0+|0|[1-9]\d*$', str(value)):
            return False, "value值输入有误,应为整数或浮点型"
        try:
            the_sensor.update({"allow_vary": float(value)})
            session.commit()
        except exc.SQLAlchemyError as e:
            session.rollback()
            return False, "传感器{0}阈值修改失败, 错误原因{1}".format(sensor_id, e)
        return True, "传感器{0} 阈值成功修改为{1}".format(sensor_id, value)
       
