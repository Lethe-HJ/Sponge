# coding: utf-8

from sqlalchemy import Integer, Date, Unicode, Numeric, exc, DateTime

from flask import g

from sqlalchemy import Column, DateTime, String, desc, and_
from . import Base
from .t_work_introduction import TWorkIntroduction as TbIntro
from .t_project_summary import TProjectSummary as TbProject
from .t_staff import TStaff
from front import session
# from front.logger import error_log
from datetime import datetime


class TDailyRecord(Base):
    __tablename__ = 'T_DailyRecord'

    ID = Column(Integer, primary_key=True)
    WorkDate = Column(Date)
    Weeks = Column(Integer)
    DayInWeek = Column(Unicode(50))
    JobDescription = Column(Unicode(1000))
    WorkHours = Column(Numeric(18, 1))
    WorkMatters = Column(String(3000, 'Chinese_PRC_CI_AS'))
    StaffName = Column(Unicode(20), nullable=False)
    ProjectName = Column(Unicode(100))
    DescripNumber = Column(Integer)
    ProjectID = Column(Unicode(50))
    isdelete = Column(Integer)
    createdate = Column(DateTime, default=datetime.now())
    createuser = Column(Integer)
    updatedate = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    updateuser = Column(Integer)
    workintroId = Column(Integer)
    userid = Column(Integer)

    @staticmethod
    def his_all_daily(detail, start, end):
        """
        获取当前用户的工作日报
        :param detail: 详细与否
        :param start: 开始时间
        :param end: 结束时间
        :return: data字典
        """
        current_user = g.user.ID
        # current_user = 199
        tb_daily = TDailyRecord  # 名字太长 换个短点的名字
        # 查询当前用户的所有工作日报 按创建时间排序
        if start and end:
            start = datetime.strptime(start, '%Y-%m-%d')  # 将日期字符串格式化成日期对象
            end = datetime.strptime(end, '%Y-%m-%d')
            condition = and_(TDailyRecord.userid == current_user, TDailyRecord.WorkDate.between(start, end))
            his_dailies = session.query(tb_daily).filter(condition).order_by(desc(tb_daily.WorkDate)).all()
        else:
            his_dailies = session.query(tb_daily).filter_by(userid=current_user).order_by(desc(tb_daily.WorkDate)).all()
        return tb_daily.pack_daily_data(his_dailies, detail)

    @staticmethod
    def query_daily(detail, query=None):
        """
        获取当前用户的工作日报
        :param detail: 详细与否
        :param query: 查询的信息
        :return: data字典
        """
        tb_daily = TDailyRecord  # 名字太长 换个短点的名字
        his_dailies = tb_daily.search_bar_entries(query)  # 获取给搜索栏的条目
        return tb_daily.pack_daily_data(his_dailies, detail)

    @staticmethod
    def pack_daily_data(dailies, detail=None):
        data_li = []
        for daily in dailies:  # 遍历当前用户的所有工作简介条目
            data = {}  # 每次循环需要重新新建data字典
            data["daily_id"] = daily.ID  # 工作日报id
            # 工作简介名称
            work_intro = session.query(TbIntro.workintro).filter_by(id=daily.workintroId).first()
            data["work_intro"] = "None" if work_intro is None else work_intro[0]
            # 项目名称
            data["project_name"] = session.query(TbProject.ProjectName).filter_by(ID=daily.ProjectID).first()[0]
            data["work_date"] = str(daily.WorkDate)  # 工作日期
            if detail:  # 详细查询要多出工时,具体事项字段
                data["work_hours"] = str(daily.WorkHours)  # 工时
                data["work_matters"] = daily.WorkMatters  # 具体事项
            data_li.append(data)  # 将data字典添加到data_li数组尾部
        return data_li

    @staticmethod
    def add_daily(**kwargs):
        kwargs["userid"] = g.user.ID
        kwargs["createuser"] = g.user.ID
        kwargs["updateuser"] = g.user.ID
        kwargs["isdelete"] = 0
        daily = TDailyRecord(**kwargs)
        date_p = datetime.strptime(kwargs["WorkDate"], '%Y-%m-%d').date()
        years, daily.Weeks, daily.DayInWeek = date_p.isocalendar()  # 获取周数和星期几
        daily.JobDescription = session.query(TbIntro.workintro).filter_by(id=daily.workintroId).first()[0]
        daily.StaffName = session.query(TStaff.StaffName).filter_by(ID=g.user.ID).first()[0]
        daily.ProjectName = session.query(TbProject.ProjectName).filter_by(ID=kwargs["ProjectID"]).first()[0]
        try:
            session.add(daily)
            session.commit()
        except exc.SQLAlchemyError as e:
            session.rollback()
            return False, "工作日报数据新增失败"

    @staticmethod
    def edit_daily(daily_id, **kwargs):
        the_daily = session.query(TDailyRecord).filter_by(ID=daily_id)
        date_p = datetime.strptime(kwargs["WorkDate"], '%Y-%m-%d').date()
        kwargs["JobDescription"] = session.query(TbIntro.workintro).filter_by(id=kwargs["workintroId"]).first()[0]
        kwargs["updateuser"] = g.user.ID
        years, kwargs["Weeks"], kwargs["DayInWeek"] = date_p.isocalendar()  # 获取周数和星期几
        if the_daily.first().userid != g.user.ID:
            return False, "不能修改他人的工作简介"
        else:
            try:
                the_daily.update(kwargs)
                session.commit()
            except exc.SQLAlchemyError as e:
                session.rollback()
                return False, "工作日报数据修改失败"
            return True, "工作日报数据修改成功"

    @staticmethod
    def search_bar_entries(query):
        """
        查询给搜索栏的条目
        :return:
        """
        # 如果query是项目 查询query值相应的项目的id
        sql_0 = """
                SELECT ID
                FROM T_WorkIntroduction
                WHERE workintro LIKE :query"""
        sql_1 = """
                SELECT id
                FROM T_ProjectSummary
                WHERE ProjectName LIKE :query"""
        # 查询 (这个项目id对应的工作日报条目 或 query值为工作简介内容的)且必为当前用户创建的 工作日报条目
        sql_2 = """
                SELECT ID, workintroId, ProjectID, WorkDate, WorkHours, WorkMatters 
                FROM T_DailyRecord
                WHERE (workintroId IN ({0}) OR ProjectID IN ({1})) AND userid=:staff_id
                ORDER BY createdate DESC;
                    """.format(sql_0, sql_1)  # 嵌套查询 这个查询比较复杂 所以用原生sql来查
        args_1 = {"query": "%{}%".format(query), "staff_id": g.user.ID}
        his_dailies = session.execute(sql_2, args_1)  # @1 执行的sql代码见本文件末尾
        return his_dailies.fetchall()

    @staticmethod
    def get_the_daily(daily_id):
        data = {}  # 每次循环需要重新新建data字典
        daily = session.query(TDailyRecord).filter_by(ID=daily_id).first()
        if daily.userid != g.user.ID:
            return False, "不能查看他人的工作日报", data
        data["daily_id"] = daily.ID  # 工作日报id
        # 工作简介名称
        # 项目名称
        data["work_date"] = str(daily.WorkDate)  # 工作日期
        data["work_hours"] = str(daily.WorkHours)  # 工时
        data["work_matters"] = daily.WorkMatters  # 具体事项
        data["project_name"] = session.query(TbProject.ProjectName).filter_by(ID=daily.ProjectID).first()[0]
        data["project_id"] = daily.ProjectID  # 当前日报对应的的项目id
        data["workintro_id"] = daily.workintroId  # 当前日报对应的的工作简介id
        data["work_intro"] = session.query(TbIntro.workintro).filter_by(id=daily.workintroId).first()[0]
        return True, "数据查询成功", data
