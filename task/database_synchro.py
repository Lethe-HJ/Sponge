from sqlalchemy import or_, between
from front.models.t_work_introduction import TWorkIntroduction as Intro
from front.models.t_daily_record import TDailyRecord as Daily
from task.models import IntroId, DailyId, BlankIdHistory, session0, session1, session2
from datetime import datetime, timedelta
from sqlalchemy.sql import func


def query_intro_synchro_date():
    """
    查询副库中需要同步的intro数据
    :return:
    """
    end_time = datetime.now()
    start_time = end_time - timedelta(days=4)
    intros = session1.query(Intro).filter(Intro.update_date.between(start_time, end_time)).all()
    return intros


def intro_old_new_filter(these_intros):
    """
    分离新旧intro数据
    :param these_intros:
    :return:
    """
    new_intros = []
    old_intros = []
    for intro in these_intros:
        blank_id = session2.query(BlankIdHistory.intro_blank_id).order_by(BlankIdHistory.createdate.desc()).first()[0]
        if intro.id > blank_id:
            new_intros.append(intro)
        else:
            old_intros.append(intro)
    return new_intros, old_intros


# 新intro数据同步----------------------------------------------------------------------------------------------------
def new_intro_synchro(intros):
    """
    新增副库中的新intro记录到主库
    :return: 新增后的id的前后变化 [{"pre": 212, "new": 113141}, ]
    """
    ids = []
    args = {}
    # 新增副库中的新intro记录到主库

    for intro in intros:
        id = {}
        id["vice_id"] = intro.id  # 记住副库的id值

        args["snumber"] = intro.snumber
        args["workaddress"] = intro.workaddress
        args["workproperty"] = intro.workproperty
        args["projectid"] = intro.projectid
        args["workintro"] = intro.workintro
        args["create_date"] = intro.create_date
        args["create_user"] = intro.create_user
        args["update_date"] = intro.update_date
        args["remarks"] = intro.remarks
        args["userid"] = intro.userid
        args["username"] = intro.username

        new_intro = Intro(**args)
        session0.add(new_intro)  # 将数据添加到目的表
        session0.flush()  # flush一下 获取id
        id["main_id"] = new_intro.id  # 记住主库id值
        session0.commit()
        session0.close()
        ids.append(id)  # 将id添加到ids中
    IntroId.edit_intro_ids(ids)  # 将ids保存到intro差异对照表


# 旧intro数据同步--------------------------------------------------------------------------------------------------------
def old_intro_synchro(intros):
    args = {}
    for intro in intros:
        main_id = IntroId.query_main_id(intro.id)
        the_intro = session0.query(Intro).filter_by(id=main_id)
        args["snumber"] = intro.snumber
        args["workaddress"] = intro.workaddress
        args["workproperty"] = intro.workproperty
        args["projectid"] = intro.projectid
        args["workintro"] = intro.workintro
        args["create_date"] = intro.create_date
        args["create_user"] = intro.create_user
        args["update_date"] = intro.update_date
        args["remarks"] = intro.remarks
        args["userid"] = intro.userid
        args["username"] = intro.username
        the_intro.update(args)
        session0.commit()


# daily数据同步==========================================================================================================
def query_daily_synchro_date():
    """
    查询副库中需要同步的daily数据
    :return:
    """
    end_time = datetime.now()
    start_time = end_time - timedelta(days=4)
    dailies = session1.query(Daily).filter(Daily.updatedate.between(start_time, end_time)).all()
    return dailies


def daily_old_new_filter(these_dailies):
    """
    分离新旧daily数据
    :param these_dailies:
    :return:
    """
    new_dailies = []
    old_dailies = []
    for daily in these_dailies:
        blank_id = session2.query(BlankIdHistory.daily_blank_id).order_by(BlankIdHistory.createdate.desc()).first()[0]
        if daily.ID > blank_id:
            new_dailies.append(daily)
        else:
            old_dailies.append(daily)
    return new_dailies, old_dailies


# 新daily数据同步----------------------------------------------------------------------------------------------------
def new_daily_synchro(dailies):
    args = dict()
    ids = []
    for daily in dailies:
        id = {}
        intro_main_id = IntroId.query_main_id(daily.workintroId)  # 根据日报的简介id从intro_id对照表中获取主库中的对应的intro_id
        args["WorkDate"] = daily.WorkDate
        args["Weeks"] = daily.Weeks
        args["DayInWeek"] = daily.DayInWeek
        args["JobDescription"] = daily.JobDescription
        args["WorkHours"] = daily.WorkHours
        args["WorkMatters"] = daily.WorkMatters.encode('latin-1').decode('gbk')
        args["StaffName"] = daily.StaffName
        args["ProjectName"] = daily.ProjectName
        args["DescripNumber"] = daily.DescripNumber
        args["ProjectID"] = daily.ProjectID
        args["isdelete"] = daily.isdelete
        args["createdate"] = daily.createdate
        args["createuser"] = daily.createuser
        args["updatedate"] = daily.updatedate
        args["updateuser"] = daily.updateuser
        args["workintroId"] = intro_main_id
        args["userid"] = daily.userid
        new_daily = Daily(**args)
        session0.add(new_daily)
        session0.flush()
        id["main_id"] = new_daily.ID
        id["vice_id"] = daily.ID
        ids.append(id)
        session0.commit()
    DailyId.edit_daily_ids(ids)


# 旧daily数据同步----------------------------------------------------------------------------------------------------
def old_daily_synchro(dailies):
    args = dict()
    for daily in dailies:
        intro_main_id = IntroId.query_main_id(dailies.workintroId)  # 根据日报的简介id从intro_id对照表中获取主库中的对应的intro_id
        daily_main_id = DailyId.query_main_id(dailies.ID)  # 查找本副库daily ID在主库中对应的daily ID值
        the_daily = session0.query(Daily).filter_by(ID=daily_main_id).first()
        args["WorkDate"] = daily.WorkDate
        args["Weeks"] = daily.Weeks
        args["DayInWeek"] = daily.DayInWeek
        args["JobDescription"] = daily.JobDescription
        args["WorkHours"] = daily.WorkHours
        args["WorkMatters"] = daily.WorkMatters.encode('latin-1').decode('gbk')
        args["StaffName"] = daily.StaffName
        args["ProjectName"] = daily.ProjectName
        args["DescripNumber"] = daily.DescripNumber
        args["ProjectID"] = daily.ProjectID
        args["isdelete"] = daily.isdelete
        args["createdate"] = daily.createdate
        args["createuser"] = daily.createuser
        args["updatedate"] = daily.updatedate
        args["updateuser"] = daily.updateuser
        args["workintroId"] = intro_main_id
        args["userid"] = daily.userid
        the_daily.update(**args)
        session0.commit()


def add_blank_id():
    intro_blank_id = session1.query(func.max(Intro.id)).first()[0] + 1
    daily_blank_id = session1.query(func.max(Daily.ID)).first()[0] + 1
    blank_arg = {"intro_blank_id": intro_blank_id,
                 "daily_blank_id": daily_blank_id,
                 "createdate": datetime.now()
                 }
    session2.add(BlankIdHistory(**blank_arg))
    session2.commit()


if __name__ == "__main__":

    intros_data = query_intro_synchro_date()  # 查询副库中需要同步的intro数据
    new_intro, old_intro = intro_old_new_filter(intros_data)  # 分离新旧数据
    new_intro_synchro(new_intro)  # 新增新数据
    old_intro_synchro(old_intro)  # 更新旧数据

    dailies_data = query_daily_synchro_date()  # 查询副库中需要同步的intro数据
    new_daily, old_daily = daily_old_new_filter(dailies_data)  # 分离新旧数据
    new_daily_synchro(new_daily)  # 新增新数据
    old_intro_synchro(old_intro)  # 更新旧数据

    add_blank_id()
