# coding: utf-8
from front.models import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, exc
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

    node = relationship('Node', primaryjoin='Sensor.nid == Node.nid', backref='sensors')
    sensor_type = relationship('SensorType', primaryjoin='Sensor.type == SensorType.id', backref='sensors')

    @staticmethod
    def get_all_sensors():
        sensors = session.query(Sensor).outerjoin(Node, Node.nid == Sensor.nid)\
            .outerjoin(SensorType, SensorType.id == Sensor.type).all()
        return [{"name": s.name, "sid": s.sid, "nid": s.node.nid, "sname": s.node.name, "location": s.node.location,
                 "status": s.node.status, "type": s.sensor_type.name} for s in sensors]
