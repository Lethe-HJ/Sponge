# coding: utf-8
from sqlalchemy.orm import relationship
from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, String, Table, Text, text, Unicode
from sqlalchemy.dialects.mysql.enumerated import ENUM
from flask import current_app, g
from sqlalchemy.dialects.mysql import BIGINT, JSON, ENUM, INTEGER, TIMESTAMP, TINYINT, VARCHAR
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from front import db
from front.libs.aes import encrypt_oracle, decrypt_oracle
from sqlalchemy import CHAR, Column, DateTime, String, or_
from front import app, cache
from . import Base, metadata


class TBusinessUnit(Base):
    __tablename__ = 'T_BusinessUnit'

    ID = Column(Integer, primary_key=True)
    BusinessUnit = Column(Unicode(20), nullable=False)
    SubDepartment = Column(Unicode(50))
    Createdate = Column(DateTime)
    Updatedate = Column(DateTime)
