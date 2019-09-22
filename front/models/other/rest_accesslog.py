# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
engine = create_engine('sqlite:///accesslog.db')
Base = declarative_base()
DBsession = sessionmaker(bind=engine)
session = DBsession()


class RestAccesslog(Base):
    __tablename__ = 'accesslog'

    Id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=True, default="NULL")
    remote_addr = Column(String(255))
    tm = Column(DateTime)
    method = Column(String(255))
    url = Column(String(255))
    description = Column(String(255), nullable=True, default="NULL")
    duration = Column(Integer, nullable=True, default=0)
    status = Column(Integer, nullable=True, default=0)
    length = Column(Integer, nullable=True, default=0)
    error_message = Column(String(255))


if __name__ == "__main__":
    Base.metadata.create_all(engine)
