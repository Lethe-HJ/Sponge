# coding: utf-8
from sqlalchemy.orm import relationship
from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, String, Table, Text, text, Unicode
from sqlalchemy.dialects.mysql.enumerated import ENUM
from flask import current_app, g
from sqlalchemy.dialects.mysql import BIGINT, JSON, ENUM, INTEGER, TIMESTAMP, TINYINT, VARCHAR
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from front import session
from front.libs.aes import encrypt_oracle, decrypt_oracle
from sqlalchemy import CHAR, Column, DateTime, String, or_
from front import app, cache
from . import Base, metadata
# from front.logger import error_log


class TWorkProperty(Base):
    __tablename__ = 'T_WorkProperty'

    id = Column(Integer, primary_key=True)
    workpropertyname = Column(Unicode(50))
    remarks = Column(Unicode(200))
    create_date = Column(DateTime)
    create_user = Column(Integer)

    @staticmethod
    def all_properties():
        """
        查询工作性质
        :return: [{"id": ***, "name": ***}, ... ]
        """
        tb_property = TWorkProperty
        # 查询工作性质
        properties = session.query(tb_property.id, tb_property.workpropertyname).all()
        return [{"id": i[0], "name": i[1]} for i in properties]  # 列表生成