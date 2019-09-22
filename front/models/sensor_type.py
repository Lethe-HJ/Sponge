from sqlalchemy import Column, String, Integer
from front.models import Base
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from flask import current_app
from front import app, cache


class SensorType(Base):
    __tablename__ = 'sensor_type'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    notes = Column(String(50), nullable=False)
