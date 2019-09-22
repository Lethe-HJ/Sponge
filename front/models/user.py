# coding: utf-8
from sqlalchemy import text
from sqlalchemy.dialects.mysql import INTEGER, TIMESTAMP, VARCHAR
from sqlalchemy import Column, String
from front.models import Base
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from flask import current_app
from front import app, cache


class User(Base):
    __tablename__ = 'user'

    id = Column(INTEGER(11), primary_key=True, comment='id')
    username = Column(VARCHAR(64), nullable=False, comment='用户名')
    password = Column(String(32), nullable=False, comment='密码')
    access_level = Column(INTEGER(255), server_default=text("1"), comment='权限等级')
    last_login = Column(TIMESTAMP, server_default=text("current_timestamp()"), comment='上次登录时间')
    create_time = Column(TIMESTAMP, server_default=text("current_timestamp()"), comment='创建时间')

    def verify_password(self, password):
        return self.password == password

    def generate_auth_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id}).decode('ascii')

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