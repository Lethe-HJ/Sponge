# coding: utf-8
from sqlalchemy import CHAR, Column, DECIMAL, Date, DateTime, Float, ForeignKey, Index, JSON, String, TIMESTAMP,\
    Table, Text, text, exc, Unicode, Integer
from sqlalchemy.dialects.mysql import BIGINT, ENUM, INTEGER, TIMESTAMP, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy import CHAR, Column, DateTime, String, or_, and_, desc
from . import Base, metadata
from .t_project_summary import TProjectSummary as TbProject
from .t_work_property import TWorkProperty
from .t_staff import TStaff
from front import session
from flask import current_app, g
# from front.logger import error_log
from datetime import datetime
from sqlalchemy.sql import func


class TWorkIntroduction(Base):
    __tablename__ = 'T_WorkIntroduction'

    id = Column(Integer, primary_key=True)
    snumber = Column(Integer)
    workaddress = Column(Integer, server_default=text("((0))"))
    workproperty = Column(Integer)
    projectid = Column(Unicode(50))
    workintro = Column(Unicode(100))
    create_date = Column(DateTime, default=datetime.now())
    create_user = Column(Integer)
    update_date = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    remarks = Column(Unicode(100))
    userid = Column(Integer)
    username = Column(Unicode(50))

    @staticmethod
    def search_entries_projects(query):
        """
        查询给搜索栏的条目
        :return:
        """
        # 如果query是项目 查询query值相应的项目的id
        sql_0 = """
            SELECT ID
            FROM T_ProjectSummary
            WHERE ProjectName LIKE :query"""
        # 查询 (这个项目id对应的工作简介条目 或 query值为工作简介内容的)且必为当前用户创建的 工作简介条目
        sql_1 = """
            SELECT id, workintro, projectid, workaddress, workproperty, userid
            FROM T_WorkIntroduction
            WHERE (workintro LIKE :query OR projectid IN ({0})) AND userid=:userid
            ORDER BY create_date DESC;
                """.format(sql_0)  # 嵌套查询 这个查询比较复杂 所以用原生sql来查
        args_1 = {"query": "%{}%".format(query), "userid": g.user.ID}
        his_intros = session.execute(sql_1, args_1)  # @1 执行的sql代码见本文件末尾
        return his_intros.fetchall()

    @staticmethod
    def himself_intros(detail):
        """
        获取当前用户的工作简介
        :param detail: 详细与否
        :return: data字典
        """
        data_li = []
        current_user = g.user.ID
        # current_user = 199
        tb_intro = TWorkIntroduction  # 名字太长 换个短点的名字
        # 查询当前用户的所有工作简介 按创建时间排序
        his_dailies = session.query(tb_intro).filter_by(userid=current_user) \
            .order_by(desc(tb_intro.create_date)).all()
        return tb_intro.pack_intro_data(his_dailies, detail)

    @staticmethod
    def query_daily(detail, query=None):
        """
        查询当前用户的工作简介
        :param detail: 详细与否
        :param query: 查询的信息
        :return: data字典
        """
        tb_intro = TWorkIntroduction  # 名字太长 换个短点的名字
        his_intros = tb_intro.search_entries_projects(query)  # 获取给搜索栏的条目
        data = tb_intro.pack_intro_data(his_intros, detail)
        message = "无此信息,请换个词试试" if data == [] else "信息查询成功"
        return True, message, data

    @staticmethod
    def pack_intro_data(intros, detail=None):
        data_li = []
        for intro in intros:  # 遍历当前用户的所有工作简介条目
            data = dict()  # 每次循环需要重新新建data字典
            data["intro_id"] = intro.id  # 工作日报id
            # 项目名称
            data["project_name"] = session.query(TbProject.ProjectName).filter_by(ID=intro.projectid).first()[0]
            data["work_intro"] = intro.workintro  # 工作日期
            if detail:  # 详细查询要多出工时,具体事项字段
                data["work_address"] = intro.workaddress  # 工作地址
                data["work_property"] = session.query(TWorkProperty.workpropertyname) \
                    .filter_by(id=intro.workproperty).first()
            data_li.append(data)  # 将data字典添加到data_li数组尾部

        return data_li

    @staticmethod
    def his_all_intros():
        tb_intro = TWorkIntroduction  # 名字太长 换个短点的名字
        his_intros = session.query(tb_intro.id, tb_intro.workintro).filter_by(userid=g.user.ID).all()
        return [{"id": i.id, "name": i.workintro} for i in his_intros]  # 列表生成
        # 结构[{},] 示例 [{"id": 9676, "name": '美签项目 自动填表功能技术验证'},]

    @staticmethod
    def fuzzy_query_by_name(project_id, query_like):
        """
        查询工作简介名称中含query_like的条目(且属于当前项目,可选) 并按照日期降序排列
        :param query_like: 限制条件 like查询字符串
        :param project_id: 限制条件 项目id
        :return:[{"id": ***, "name": ***}, ... ]
        """
        tb_intros = TWorkIntroduction
        # 查询工作简介名称中含query_like的条目的id与work_intro
        condition = and_(tb_intros.workintro.like(query_like), tb_intros.userid == g.user.ID)
        if project_id:  # 如果有project_id 则将其加入and条件中
            condition = and_(condition, tb_intros.projectid == project_id)
        intros = session.query(tb_intros.id, tb_intros.workintro) \
            .filter(condition).order_by(desc(tb_intros.create_date)).all()
        return [{"id": i[0], "name": i[1]} for i in intros]  # 列表生成

    @staticmethod
    def add_intro(**intro):
        Intro = TWorkIntroduction
        the_intro = TWorkIntroduction(**intro)
        the_intro.userid = g.user.ID
        the_intro.create_user = g.user.ID
        the_intro.username = session.query(TStaff.StaffName).filter_by(ID=g.user.ID).first()[0]
        the_intro.snumber = session.query(func.max(Intro.snumber)).first()[0] + 1
        try:
            session.add(the_intro)
            session.commit()
        except exc.SQLAlchemyError as e:
            session.rollback()
            return False, "数据提交失败"
        return True, "数据提交成功"

    @staticmethod
    def edit_intro(intro_id, **kwargs):
        tb_intro = TWorkIntroduction  # 名字太长 换个短点的名字
        the_intro = session.query(tb_intro).filter_by(id=intro_id)
        if the_intro.first().userid != g.user.ID:
            return False, "不能修改他人创建的工作简介"
        else:
            try:
                the_intro.update(kwargs)
                session.commit()
            except exc.SQLAlchemyError as e:
                session.rollback()
                raise e
                # return False, "工作简介数据修改失败"
            return True, "工作简介修改成功"

    @staticmethod
    def get_the_intro(intro_id):
        data = {}  # 每次循环需要重新新建data字典
        intro = session.query(TWorkIntroduction).filter_by(id=intro_id).first()
        if intro is None:
            return False, "无此工作简介", data
        if intro.userid != g.user.ID:
            return False, "不能查看他人的工作简介", data
        data["intro_id"] = intro.id  # 工作简介id
        data["work_intro"] = intro.workintro  # 工作简介名称
        data["project_id"] = intro.projectid  # 工作简介id
        data["project_name"] = session.query(TbProject.ProjectName) \
            .filter_by(ID=intro.projectid).first()[0]  # 项目名称
        data["work_address"] = intro.workaddress  # 工作地址
        # 查询这个工作简介对应的工作性质
        the_property = session.query(TWorkProperty.workpropertyname, TWorkProperty.id) \
            .filter_by(id=intro.workproperty).first()
        if the_property is None:
            data["work_property"], data["work_property_id"] = "无", 0
        else:
            data["work_property"], data["work_property_id"] = the_property.workpropertyname, the_property.id
        data["remarks"] = intro.remarks  # 备注
        return True, "数据查询成功", data

    @staticmethod
    def intros_of_project(project_id):
        tb_intro = TWorkIntroduction  # 名字太长 换个短点的名字
        # 查询当前项目 当前用户对应 的工作简介
        his_intros = session.query(tb_intro.id, tb_intro.workintro) \
            .filter(and_(tb_intro.create_user == g.user.ID, tb_intro.projectid == project_id)) \
            .order_by(desc(tb_intro.create_date)).all()
        return [{"id": i.id, "name": i.workintro} for i in his_intros]  # 列表生成

    @staticmethod
    def search_his_intros(query_like, project_id):
        # 查询用户的工作简介名称中含query_like的条目的id与work_intro
        tb_intro = TWorkIntroduction  # 名字太长 换个短点的名字
        query_like = "%{}%".format(query_like)
        intros = session.query(tb_intro.id, tb_intro.workintro) \
            .filter(and_(tb_intro.workintro.like(query_like), tb_intro.create_user == g.user.ID,
                         tb_intro.projectid == project_id)) \
            .order_by(desc(tb_intro.create_date)).all()
        data = [{"id": i[0], "name": i[1]} for i in intros]  # 列表生成
        return data
        # 结构[{},] 示例 [{"id": 9676, "name": '美签项目 自动填表功能技术验证'},]

    @staticmethod
    def history_projects_in_intros():
        tb_intro = TWorkIntroduction
        # 查询该用户的工作简介出现的项目id集合
        project_ids = session.query(tb_intro.projectid).filter(tb_intro.create_user == g.user.ID).distinct().all()
        # 修改数据结构 [(id,),] -> [id,]
        project_ids = [ids[0] for ids in project_ids]
        # 查询前面id集合对应的项目Id与项目名组成的集合 按时间降序排列
        projects = session.query(TbProject.ID, TbProject.ProjectName).filter(TbProject.ID.in_(project_ids))\
            .order_by(desc(TbProject.create_date)).distinct().all()
        return projects

# @1处的查询sql语句
# SELECT id, work_intro, project_id, work_address, work_property_id
# FROM t_work_introduction
# WHERE (work_intro='东航公务证件管理系统'
#   OR
#       project_id = (
#           SELECT id
#           FROM t_project_summary
#           WHERE project_name='东航公务证件管理系统'
#           LIMIT 1))
#   AND
#       staff_id = 199;
