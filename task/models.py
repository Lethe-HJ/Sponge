from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta
import pymssql
from sqlalchemy import Column, Integer, String, DateTime


# 主库
SQLALCHEMY_DATABASE_URI0 = 'mssql+pymssql://sa:wVYV7denNPOJntZ@47.106.83.135:1433/workdailyformalCopy?charset=utf8'
engine0 = create_engine(SQLALCHEMY_DATABASE_URI0)
DBsession0 = sessionmaker(bind=engine0)
session0 = DBsession0()

# 副库
SQLALCHEMY_DATABASE_URI1 = 'mssql+pymssql://sa:wVYV7denNPOJntZ@47.106.83.135:1433/workdailyformal?charset=utf8'
# SQLALCHEMY_DATABASE_URI1 = 'mssql+pymssql://hujing:wVYV7denNPOJntZ@10.200.51.18:1433/workdailyformal?charset=utf8'
engine1 = create_engine(SQLALCHEMY_DATABASE_URI1)
DBsession1 = sessionmaker(bind=engine1)
session1 = DBsession1()

# sqlite 主副库关联
engine2 = create_engine('sqlite:///id.db')
Base = declarative_base()
DBsession2 = sessionmaker(bind=engine2)
session2 = DBsession2()


class IntroId(Base):
    __tablename__ = 'intro_id'
    id = Column(Integer, primary_key=True)
    vice_id = Column(Integer)  # 副库id
    main_id = Column(Integer, )  # 主库id

    @staticmethod
    def query_main_id(vice_id):
        """
        根据vice_id查找main_id
        :param vice_id:
        :return:
        """
        main_id = session2.query(IntroId.main_id).filter_by(vice_id=vice_id).first()
        main_id = vice_id if main_id is None else main_id[0]
        return main_id

    @staticmethod
    def edit_intro_ids(intro_ids):
        for intro_id in intro_ids:
            query = session2.query(IntroId).filter_by(vice_id=intro_id["vice_id"]).first()
            if query is None:
                session2.add(IntroId(**intro_id))
                session2.commit()
            else:
                query.main_id = intro_id["main_id"]
                session2.commit()


class DailyId(Base):
    __tablename__ = 'daily_id'
    id = Column(Integer, primary_key=True)
    vice_id = Column(Integer)  # 副库id
    main_id = Column(Integer)  # 主库id

    @staticmethod
    def query_main_id(vice_id):
        """
        根据vice_id查找main_id
        :param vice_id:
        :return:
        """
        main_id = session2.query(DailyId.main_id).filter_by(vice_id=vice_id).first()
        return main_id

    @staticmethod
    def edit_daily_ids(daily_ids):
        for daily_id in daily_ids:
            query = session2.query(DailyId).filter_by(vice_id=daily_id["vice_id"])
            if query.first() is None:
                session2.add(DailyId(**daily_id))
                session2.commit()
            else:
                query.main_id = daily_id["main_id"]
                session2.commit()


class BlankIdHistory(Base):  # 新旧数据分割表
    __tablename__ = 'blank_id'
    id = Column(Integer, primary_key=True)
    intro_blank_id = Column(Integer)
    daily_blank_id = Column(Integer)
    createdate = Column(DateTime, default=datetime.now())


if __name__ == "__main__":
    Base.metadata.create_all(engine2)
