# coding: utf-8
from sqlalchemy.orm import relationship
from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, String, Table, Text, text, Unicode
from sqlalchemy.dialects.mysql.enumerated import ENUM
from flask import current_app
from sqlalchemy.dialects.mysql import BIGINT, JSON, ENUM, INTEGER, TIMESTAMP, TINYINT, VARCHAR
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from front import db
from front.libs.aes import encrypt_oracle, decrypt_oracle
from sqlalchemy import CHAR, Column, DateTime, String, or_
from front import app, cache
from . import Base, metadata
from .t_business_unit import TBusinessUnit
# from front.logger import error_log


class TStaff(Base):
    __tablename__ = 'T_Staff'

    ID = Column(Integer, primary_key=True)
    StaffName = Column(Unicode(20))
    Department = Column(Unicode(20))
    SerialNum = Column(Integer)
    LoginPassword = Column(Unicode(50))
    Classifiation = Column(Unicode(50))
    sex = Column(Integer)
    StaffCode = Column(Unicode(50))
    StaffPhone = Column(Unicode(20))
    position = Column(Unicode(20))
    staffrole = Column(Integer)
    isdelete = Column(Integer)
    create_date = Column(DateTime)
    update_date = Column(DateTime)
    create_user = Column(Integer)
    update_user = Column(Integer)
    StaffStatus = Column(Integer)
    remarks = Column(Unicode(200))
    isUpdate = Column(Integer)
    BusinessUnit = Column(Integer)
    DepartMentId = Column(Integer)
    StaffAuth = Column(Integer)
    ManageDepartmentId = Column(String(4096, 'Chinese_PRC_CI_AS'))
    ManageStaffId = Column(String(4096, 'Chinese_PRC_CI_AS'))

    def init_password(self):
        self.device_password = encrypt_oracle(current_app.config.get("INIT_PASSWORD", "xd12345678"),
                                              current_app.config.get("AES_KEY", "12345678"))

    def encode_password(self, password):
        # 加密密码
        self.device_password = encrypt_oracle(password, current_app.config.get("AES_KEY", "12345678"))

    def decode_password(self):
        # 解密密码
        return decrypt_oracle(self.device_password, current_app.config.get("AES_KEY", "12345678"))

    def verify_password(self, password):
        return self.LoginPassword == self.delete_zero(password)

    def delete_zero(self, md5_str):
        new_str = ""
        for i in range(0, len(md5_str), 2):
            num_s = md5_str[i:i + 2]
            if num_s[0] == "0" and int(num_s[1], 16) > 9:

                new_str += num_s[1]
            else:
                new_str += num_s
        return new_str

    def generate_auth_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.ID}).decode('ascii')

    def save_token(self, id, token):
        cache.set(id, token, timeout=3600)



    @staticmethod
    def verify_parse_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valId token, but expired
        except BadSignature:
            return None  # invalId token
        # user = db.session.query(UUser).get(data['id'])
        return data