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
    address = Column(String(255))
    location = Column(String(255))
    status = Column(Integer)
    secret_key = Column(String(30))

    @staticmethod
    def get_all_nodes():
        nodes = session.query(Node).all()
        return True, "数据获取成功", [{"nid": n.nid, "name": n.address,
         "location": n.location, "status": n.status} for n in nodes]
    
    @staticmethod
    def get_the_node(nid):
        node = session.query(Node).filter_by(nid=nid).first()
        if not node:
            return False, "无此基站"
        return True, "数据获取成功", {"nid": node.nid, "name": node.address,
         "location": node.location, "status": node.status}

    @staticmethod
    def edit_node(nid, args):
        the_node = session.query(Node).filter_by(nid=nid)
        if not the_node.first():  # 记录不存在
            return False, "无此基站"
        try:
            the_node.update(args)
            session.commit()
        except exc.SQLAlchemyError as e:
            session.rollback()
            return False, "基站{0}数据修改失败, 错误原因{1}".format(nid, e)
        return True, "基站{0} 数据成功修改为{1}".format(nid, args)

    def node_eidt_args_check(self, nid, args):
        msg_li = []

        # 参数缺失处理
        if not nid:
            msg_li.append("nid")
        msg_li += self.node_args_exit_check(args)
        if msg_li != []:
            return False, "缺少参数" + ",".join(msg_li)

        # 参数值检验
        if not re.match(r"[1-9]\d*|0", str(nid)):
            return False, "nid参数的值需为十进制数字"
        # address, location, status, secret_key的参数检查,后续再补
        return True, "参数检测成功"

    def node_add_args_check(self, args):
        # 参数缺失处理
        msg_li = self.node_args_exit_check(args)
        if msg_li != []:
            return False, "缺少参数" + ",".join(msg_li)

        # address, location, status, secret_key的参数检查,后续再补
        return True, "参数检测成功"

    @staticmethod
    def add_node(args):
        node_new = Node(**args)
        try:
            session.add(node_new)
            session.commit()
        except exc.SQLAlchemyError as e:
            session.rollback()
            return False, "数据提交失败，失败原因为{0}".format(e)
        return True, "数据提交成功，成功新增基站{0}".format(args)

    def node_args_exit_check(self, args):
        msg_li = []
        # 参数缺失处理
        if not args["address"]:
            msg_li.append("address")
        if not args["location"]:
            msg_li.append("location")
        if not args["status"]:
            msg_li.append("status")
        if not args["secret_key"]:
            msg_li.append("secret_key")
        # address, location, status, secret_key的参数检查,后续再补
        return msg_li