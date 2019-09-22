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


class Node(Base):
    __tablename__ = 'nodes'

    nid = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    location = Column(String(255))
    status = Column(Integer)

    @staticmethod
    def get_all_nodes():
        nodes = session.query(Node).all()
        return True, "数据获取成功", [{"nid": n.nid, "name": n.name, "location": n.location, "status": n.status} for n in nodes]
