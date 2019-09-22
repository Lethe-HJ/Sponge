# coding: utf-8
from sqlalchemy.orm import relationship
from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, String, Table, Text, text, Unicode, Date
from sqlalchemy.dialects.mysql.enumerated import ENUM
from flask import current_app, g
from sqlalchemy.dialects.mysql import BIGINT, JSON, ENUM, INTEGER, TIMESTAMP, TINYINT, VARCHAR
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from front import db
from front.libs.aes import encrypt_oracle, decrypt_oracle
from sqlalchemy import CHAR, Column, DateTime, String, or_, desc
from front import app, cache
from front.models import Base, metadata
from front import session
# from front.logger import error_log


class TProjectSummary(Base):
    __tablename__ = 'T_ProjectSummary'

    ID = Column(Unicode(50), primary_key=True)
    ProductType = Column(Unicode(50))
    SNumber = Column(Integer)
    ProjectNumber = Column(Unicode(50))
    ProjectName = Column(Unicode(100))
    ProductModel = Column(Unicode(100))
    ProjectManager = Column(Unicode(50))
    Classifiation = Column(Unicode(50))
    ProjectAlias = Column(Unicode(100), index=True)
    OAOder = Column(Unicode(100))
    isdelete = Column(Integer, server_default=text("((0))"))
    create_date = Column(DateTime)
    update_date = Column(DateTime)
    create_user = Column(Unicode(50))
    update_user = Column(Unicode(50))
    ProjectStatus = Column(Integer, server_default=text("((0))"))
    ProjectTypeID = Column(Integer)
    remarks = Column(Unicode(200))
    enteringdate = Column(Date)
    Status = Column(Unicode(10))
    leadparty = Column(Unicode(50))
    EndTime = Column(DateTime)
    ErpID = Column(Unicode(50))
    NewOrOldID = Column(Integer, server_default=text("((1))"))

    @staticmethod
    def all_projects(items):
        tb_project = TProjectSummary
        projects = session.query(tb_project.ID, tb_project.ProjectName) \
            .order_by(desc(tb_project.create_date))
        if not items:  # 默认返回所有的数条目
            projects = projects.all()  # 获取所有的项目数据
        else:
            projects = projects.limit(items).all()  # 获取最新的items条项目数据
        return [(i[0], i[1]) for i in projects]  # 列表生成
        # 结构[{},] 示例 [{"id": '005d5b45-4e34-4eb9-b68b-30e0199b6aa5', "name": '宝鸡二维码改造'},]

    @staticmethod
    def fuzzy_query_by_name(query_like):
        """
        查询项目名称中含query_like的条目 并按照日期降序排列
        :param query_like: like查询字符串
        :return:[{"id": ***, "name": ***}, ... ]
        """
        tb_project = TProjectSummary
        # 查询项目名称中含query_like的条目的id与project_name
        query_like = "%{}%".format(query_like)
        projects = session.query(tb_project.ID, tb_project.ProjectName) \
            .filter(tb_project.ProjectName.like(query_like)) \
            .order_by(desc(tb_project.create_date)).all()
        data = [{"id": i[0], "name": i[1]} for i in projects]  # 列表生成
        return True, "数据查询成功", data


