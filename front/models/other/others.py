# coding: utf-8
from sqlalchemy import CHAR, Column, DECIMAL, Date, DateTime, Float, ForeignKey, Index, JSON, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, ENUM, INTEGER, TIMESTAMP, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class KqUserInfo(Base):
    __tablename__ = 'kq_user_info'

    user_id = Column(BIGINT(20), primary_key=True, comment='员工id')
    badge_number = Column(String(24, 'utf8_croatian_ci'), nullable=False, comment='工号')
    name = Column(String(40, 'utf8_croatian_ci'), comment='员工名称')
    gender = Column(ENUM('M', 'F', ''), comment='性别：M 男 F 女')
    notes = Column(String(500, 'utf8_croatian_ci'), comment='备注')


class OaNotify(Base):
    __tablename__ = 'oa_notify'

    id = Column(BIGINT(20), primary_key=True, comment='编号')
    type = Column(CHAR(1, 'utf8_bin'), comment='类型')
    title = Column(String(200, 'utf8_bin'), comment='标题')
    content = Column(String(2000, 'utf8_bin'), comment='内容')
    files = Column(String(2000, 'utf8_bin'), comment='附件')
    status = Column(CHAR(1, 'utf8_bin'), comment='状态')
    create_by = Column(BIGINT(20), comment='创建者')
    create_date = Column(DateTime, comment='创建时间')
    update_by = Column(String(64, 'utf8_bin'), comment='更新者')
    update_date = Column(DateTime, comment='更新时间')
    remarks = Column(String(255, 'utf8_bin'), comment='备注信息')
    del_flag = Column(CHAR(1, 'utf8_bin'), index=True, server_default=text("'0'"), comment='删除标记')


class OaNotifyRecord(Base):
    __tablename__ = 'oa_notify_record'

    id = Column(BIGINT(20), primary_key=True, comment='编号')
    notify_id = Column(BIGINT(20), index=True, comment='通知通告ID')
    user_id = Column(BIGINT(20), index=True, comment='接受人')
    is_read = Column(TINYINT(1), index=True, server_default=text("'0'"), comment='阅读标记')
    read_date = Column(Date, comment='阅读时间')


class RestAccesslog(Base):
    __tablename__ = 'rest_accesslog'

    Id = Column(INTEGER(11), primary_key=True)
    name = Column(String(255), comment='客户端')
    remote_addr = Column(String(255), comment='客户端IP')
    tm = Column(DateTime, comment='访问时间')
    method = Column(String(255), comment='方法，GET,PUT,POST,DELETE')
    url = Column(String(255), comment='资源')
    description = Column(String(255), comment='描述')
    duration = Column(INTEGER(11), comment='处理时长（毫秒）')
    status = Column(INTEGER(11), comment='HTTP状态码')
    length = Column(INTEGER(11), comment='报文长度')
    error_message = Column(Text, comment='错误信息')


class RestRtable(Base):
    __tablename__ = 'rest_rtable'

    Id = Column(INTEGER(11), primary_key=True, nullable=False)
    funcode = Column(String(255), primary_key=True, nullable=False, server_default=text("''"), comment='code')
    xpath = Column(String(255), comment='访问url')
    description = Column(String(255), comment='备注')


class RestUser(Base):
    __tablename__ = 'rest_user'

    Id = Column(INTEGER(11), primary_key=True)
    name = Column(String(255), comment='客户端账号')
    password_hash = Column(String(255), comment='密码（SHA256）')
    ip = Column(String(255), comment='限定IP地址')
    vendor = Column(String(255), comment='厂商')


class RptFilter(Base):
    __tablename__ = 'rpt_filter'

    Id = Column(INTEGER(11), primary_key=True)
    report_id = Column(INTEGER(11), comment='报表ID')
    name = Column(String(255), comment='字段名称')
    ui_label = Column(String(255), comment='标签文字')
    ui_type = Column(String(255), comment='UI显示类型(INPUT, SELECT, DATE)')
    default_value = Column(String(255), comment='默认值')
    sql = Column(String(4000), comment='下拉过滤时，从字典表查询下拉项')
    ord = Column(INTEGER(11), comment='显示位置')
    is_number = Column(INTEGER(11), comment='是否数值字段（作为查询条件时，不带引号）')
    options = Column(String(255), comment='配置项')
    pname = Column(String(255), comment='级联查询时，父节点名称')
    is_required = Column(INTEGER(11), comment='必填选项')


class RptHeader(Base):
    __tablename__ = 'rpt_header'

    Id = Column(INTEGER(11), primary_key=True)
    report_id = Column(INTEGER(11), comment='报表ID')
    name = Column(String(255), comment='字段名称')
    title = Column(String(255), comment='界面显示的名称')
    ord = Column(INTEGER(11), comment='显示位置')
    grouped = Column(INTEGER(11), comment='0 - 不分组，1 - 分组')
    acc = Column(INTEGER(11), comment='是否计算小计合计，0 - 否，1 - 是')
    column_width = Column(INTEGER(11), comment='列宽')
    is_decimal = Column(INTEGER(11), comment='是否小数字段，小数字段显示时，以%.2f进行格式化，显示2位小数')
    hide = Column(INTEGER(11), comment='是否隐藏')


class RptReport(Base):
    __tablename__ = 'rpt_report'

    Id = Column(INTEGER(11), primary_key=True)
    title = Column(String(255), comment='标题')
    sql = Column(String(4000), comment='查询SQL')
    order_by = Column(String(255), comment='排序字段')
    acc_total = Column(INTEGER(11), comment='是否显示合计，0 - 不显示，1 - 显示')
    paging = Column(INTEGER(11), comment='是否分页，0 - 分页，1 - 不分页')
    rowspan = Column(INTEGER(10), comment='是否合并单元格，0 - 不合并，1 - 合并')


class SysConfig(Base):
    __tablename__ = 'sys_config'

    Id = Column(INTEGER(11), primary_key=True)
    key = Column(String(255), nullable=False, unique=True, server_default=text("''"), comment='配置项')
    value = Column(String(255), nullable=False, server_default=text("''"), comment='值')
    remarks = Column(String(255), comment='备注说明')


class SysDept(Base):
    __tablename__ = 'sys_dept'

    dept_id = Column(BIGINT(20), primary_key=True)
    parent_id = Column(BIGINT(20), comment='上级部门ID，一级部门为0')
    name = Column(String(50), comment='部门名称')
    order_num = Column(INTEGER(11), comment='排序')
    del_flag = Column(TINYINT(4), server_default=text("'0'"), comment='是否删除  -1：已删除  0：正常')


class SysDict(Base):
    __tablename__ = 'sys_dict'
    __table_args__ = (
        Index('sys_dict_type_description', 'type', 'description'),
    )

    id = Column(BIGINT(64), primary_key=True, comment='编号')
    name = Column(String(100, 'utf8_bin'), index=True, comment='标签名')
    value = Column(String(100, 'utf8_bin'), index=True, comment='数据值')
    type = Column(String(100, 'utf8_bin'), comment='类型')
    description = Column(String(100, 'utf8_bin'), comment='描述')
    sort = Column(DECIMAL(10, 0), comment='排序（升序）')
    parent_id = Column(BIGINT(64), server_default=text("'0'"), comment='父级编号')
    create_by = Column(INTEGER(64), comment='创建者')
    create_date = Column(DateTime, comment='创建时间')
    update_by = Column(BIGINT(64), comment='更新者')
    update_date = Column(DateTime, comment='更新时间')
    remarks = Column(String(255, 'utf8_bin'), comment='备注信息')
    del_flag = Column(CHAR(1, 'utf8_bin'), index=True, server_default=text("'0'"), comment='删除标记')


class SysFile(Base):
    __tablename__ = 'sys_file'

    id = Column(BIGINT(20), primary_key=True)
    type = Column(INTEGER(11), comment='文件类型')
    url = Column(String(200), comment='URL地址')
    create_date = Column(DateTime, comment='创建时间')


class SysLog(Base):
    __tablename__ = 'sys_log'

    id = Column(BIGINT(20), primary_key=True)
    user_id = Column(BIGINT(20), comment='用户id')
    username = Column(String(50), comment='用户名')
    operation = Column(String(50), comment='用户操作')
    time = Column(INTEGER(11), comment='响应时间')
    method = Column(String(200), comment='请求方法')
    params = Column(String(5000), comment='请求参数')
    ip = Column(String(64), comment='IP地址')
    gmt_create = Column(DateTime, comment='创建时间')


class SysMenu(Base):
    __tablename__ = 'sys_menu'

    menu_id = Column(BIGINT(20), primary_key=True)
    parent_id = Column(BIGINT(20), comment='父菜单ID，一级菜单为0')
    name = Column(String(50), comment='菜单名称')
    url = Column(String(200), comment='菜单URL')
    perms = Column(String(500), comment='授权(多个用逗号分隔，如：user:list,user:create)')
    type = Column(INTEGER(11), comment='类型   0：目录   1：菜单   2：按钮')
    icon = Column(String(50), comment='菜单图标')
    order_num = Column(INTEGER(11), comment='排序')
    gmt_create = Column(DateTime, comment='创建时间')
    gmt_modified = Column(DateTime, comment='修改时间')


class SysRole(Base):
    __tablename__ = 'sys_role'

    role_id = Column(BIGINT(20), primary_key=True)
    role_name = Column(String(100), comment='角色名称')
    role_sign = Column(String(100), comment='角色标识')
    remark = Column(String(100), comment='备注')
    user_id_create = Column(BIGINT(255), comment='创建用户id')
    gmt_create = Column(DateTime, comment='创建时间')
    gmt_modified = Column(DateTime, comment='创建时间')


class SysRoleMenu(Base):
    __tablename__ = 'sys_role_menu'

    id = Column(BIGINT(20), primary_key=True)
    role_id = Column(BIGINT(20), comment='角色ID')
    menu_id = Column(BIGINT(20), comment='菜单ID')


class SysTask(Base):
    __tablename__ = 'sys_task'

    id = Column(BIGINT(20), primary_key=True)
    cron_expression = Column(String(255), comment='cron表达式')
    method_name = Column(String(255), comment='任务调用的方法名')
    is_concurrent = Column(String(255), comment='任务是否有状态')
    description = Column(String(255), comment='任务描述')
    update_by = Column(String(64), comment='更新者')
    bean_class = Column(String(255), comment='任务执行时调用哪个类的方法 包名+类名')
    create_date = Column(DateTime, comment='创建时间')
    job_status = Column(String(255), comment='任务状态')
    job_group = Column(String(255), comment='任务分组')
    update_date = Column(DateTime, comment='更新时间')
    create_by = Column(String(64), comment='创建者')
    spring_bean = Column(String(255), comment='Spring bean')
    job_name = Column(String(255), comment='任务名')


class SysUser(Base):
    __tablename__ = 'sys_user'

    user_id = Column(BIGINT(20), primary_key=True)
    username = Column(String(50), comment='用户名')
    name = Column(String(100))
    password = Column(String(50), comment='密码')
    dept_id = Column(BIGINT(20))
    email = Column(String(100), comment='邮箱')
    mobile = Column(String(100), comment='手机号')
    status = Column(TINYINT(255), comment='状态 0:禁用，1:正常')
    user_id_create = Column(BIGINT(255), comment='创建用户id')
    gmt_create = Column(DateTime, comment='创建时间')
    gmt_modified = Column(DateTime, comment='修改时间')
    sex = Column(BIGINT(32), comment='性别')
    birth = Column(DateTime, comment='出身日期')
    pic_id = Column(BIGINT(32))
    live_address = Column(String(500), comment='现居住地')
    hobby = Column(String(255), comment='爱好')
    province = Column(String(255), comment='省份')
    city = Column(String(255), comment='所在城市')
    district = Column(String(255), comment='所在地区')


class SysUserPlu(Base):
    __tablename__ = 'sys_user_plus'

    id = Column(BIGINT(20), primary_key=True)
    user_id = Column(BIGINT(20), nullable=False)
    payment = Column(Float(asdecimal=True))


class SysUserRole(Base):
    __tablename__ = 'sys_user_role'

    id = Column(BIGINT(20), primary_key=True)
    user_id = Column(BIGINT(20), comment='用户ID')
    role_id = Column(BIGINT(20), comment='角色ID')


class TAttendanceManHour(Base):
    __tablename__ = 't_attendance_man_hour'

    id = Column(String(32, 'utf8_croatian_ci'), primary_key=True, comment='主键,暂时用UUID进行自增')
    json = Column(JSON, comment='通过JSON字段进行关联查询，也方便后续扩展!')
    remarks = Column(String(255, 'utf8_croatian_ci'), comment='备注')

class TbUser(Base):
    __tablename__ = 'tb_user'

    Id = Column(INTEGER(11), primary_key=True)
    name = Column(String(255), comment='姓名')
    password_hash = Column(String(255), comment='密码（SHA256）')
    wx_openid = Column(String(255), comment='微信唯一用户标识')
    id_type = Column(INTEGER(11), comment='证件类型')
    id_no = Column(String(255), comment='证件号码')
    telephone = Column(String(255), comment='电话号码')
    last_login = Column(DateTime, comment='最后登录时间')
    last_login_ip = Column(String(255), comment='最后登录的IP地址')
    data = Column(Text, comment='JSON格式的用户数据')




class TDictType(Base):
    __tablename__ = 't_dict_type'

    id = Column(BIGINT(64), primary_key=True, comment='字段类型ID:主键,自动增长')
    type = Column(String(100, 'utf8_croatian_ci'), nullable=False, comment='类型')
    description = Column(String(100, 'utf8_croatian_ci'), nullable=False, comment='类型描述')
    remarks = Column(String(255, 'utf8_croatian_ci'), comment='备注')


class TProgramFile(Base):
    __tablename__ = 't_program_file'

    id = Column(BIGINT(20), primary_key=True, comment='程序文件表：主键ID，自动增长')
    file_name = Column(String(200, 'utf8_croatian_ci'), nullable=False, comment='文件名字')
    state = Column(String(2, 'utf8_croatian_ci'), nullable=False, comment='文件状态 1 开源文件 2 已归档')
    imprint = Column(String(500, 'utf8_croatian_ci'), comment='版本说明：每一次归档要求说明本次修改的内容')
    remark = Column(String(50, 'utf8_croatian_ci'), comment='备注')


class TProject(Base):
    __tablename__ = 't_project'

    id = Column(BIGINT(20), primary_key=True, comment='主键:项目ID,自动增长')
    pro_name = Column(String(50, 'utf8_croatian_ci'), nullable=False, comment='项目名字')
    path = Column(String(200, 'utf8_croatian_ci'), nullable=False, comment='路径')
    remark = Column(String(500, 'utf8_croatian_ci'), comment='备注')




class TbFile(Base):
    __tablename__ = 'tb_file'

    Id = Column(INTEGER(11), primary_key=True)
    filename = Column(String(255), comment='文件名')
    path = Column(String(255), comment='文件路径')
    user_id = Column(INTEGER(11), comment='用户编号')
    upload_user = Column(String(255), comment='录入人')
    upload_date = Column(DateTime, comment='录入时间')
    remarks = Column(VARCHAR(255), comment='备注信息')


class TbForm(Base):
    __tablename__ = 'tb_form'

    Id = Column(INTEGER(11), primary_key=True)
    user_id = Column(INTEGER(11), comment='用户编号')
    xm = Column(String(255), comment='填表用户姓名')
    id_type = Column(INTEGER(11), comment='证件类型')
    id_no = Column(String(255), comment='证件号码')
    form_type = Column(INTEGER(11), comment='表单类型')
    telephone = Column(String(255), comment='联系电话')
    form_date = Column(DateTime, comment='填表时间')
    form_date_num = Column(INTEGER(11), comment='填表时间的数字，例如20180802')
    meeting_date = Column(DateTime, comment='预约业务办理时间')
    hall_id = Column(INTEGER(11), comment='预约服务大厅编号')
    hall_name = Column(String(255), comment='服务大厅名称')
    data = Column(Text, comment='JSON格式的填表数据')
    upload_user = Column(String(255), comment='录入人')
    upload_date = Column(DateTime, comment='录入时间')
    sync = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='同步标志，1 - 正在同步，2 - 同步完成')
    sync_time = Column(DateTime, comment='最后一次同步的时间')
    print = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='打印标志')
    print_time = Column(DateTime, comment='打印时间')
    exam = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='审核标志，1 - 成功，2 - 失败')
    exam_time = Column(DateTime, comment='审核时间')
    deal = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='受理标志，1 - 成功，2 - 失败')
    deal_time = Column(DateTime, comment='受理时间')
    reason = Column(String(255), server_default=text("''"), comment='问题描述')
    status = Column(INTEGER(11), comment='1-正常 0-取消')
    cancel_time = Column(DateTime, comment='取消时间')
    district = Column(String(255), comment='所在地区')


class TbFormCheck(Base):
    __tablename__ = 'tb_form_check'

    Id = Column(INTEGER(11), primary_key=True)
    type = Column(INTEGER(11), comment='表单类型')
    field_name = Column(String(255), comment='字段名称，用"."分隔标示JSON中的层次关系')
    non_null = Column(INTEGER(11), comment='非空检查，0 - 不检查，1 - 检查')
    min_length = Column(INTEGER(11), comment='最小长度检查')
    max_length = Column(INTEGER(11), comment='最大长度检查，汉字算2个字符')
    digit_only = Column(INTEGER(11), comment='必须是数字，0 - 不检查，1 - 检查')
    display_name = Column(String(255), comment='显示字段名称')
    remarks = Column(String(255), comment='备注')
    sort = Column(INTEGER(11), comment='排序字段')
    digest = Column(INTEGER(1), comment='是否生成摘要')



class KqCheckInout(Base):
    __tablename__ = 'kq_check_inout'

    id = Column(BIGINT(20), primary_key=True)
    user_id = Column(ForeignKey('kq_user_info.user_id'), nullable=False, index=True, comment='员工id，外键')
    date = Column(String(50), nullable=False, comment='日期')
    office_hour = Column(String(50), server_default=text("'00:00:00'"), comment='上班时间')
    off_hours = Column(String(50), server_default=text("'00:00:00'"), comment='下班时间')
    runing_hour = Column(String(10), comment='工作时间')
    notes = Column(String(500), comment='备注')

    user = relationship('KqUserInfo')


class TDailyRecord(Base):
    __tablename__ = 't_daily_record'

    id = Column(BIGINT(20), primary_key=True, comment='每日日报ID:主键')
    work_date = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='工作时间 注:当前日期 如:2018-11.29')
    weeks = Column(BIGINT(11), comment='周 注:该年的第几周')
    day_in_week = Column(String(50, 'utf8_croatian_ci'), comment='星期几 注:一周七天 1,2,3,4,5,6,7')
    job_description = Column(String(255, 'utf8_croatian_ci'), comment='工作简介 从工作简历表获取t_work_introduction(work_intro)')
    work_hours = Column(Float(7), comment='工时 注:上班小时')
    work_matters = Column(String(3000, 'utf8_croatian_ci'), comment='工作事项 注:每天工作的内容')
    staff_name = Column(String(255, 'utf8_croatian_ci'), comment='人员姓名 从人员表中获取:t_staff(saff_name)')
    project_name = Column(String(255, 'utf8_croatian_ci'), comment='项目名称 从项目表中获取t_project_summary(project_name) 注:主要方便查询!')
    descrip_number = Column(BIGINT(11), comment='工作简介序号 从工作简历表获取t_work_introduction(s_number)')
    project_id = Column(String(255, 'utf8_croatian_ci'), index=True, comment='项目ID 外键:t_project_summary(id)')
    isdelete = Column(BIGINT(11), server_default=text("'0'"), comment='是否已删除 0：否 1:是')
    create_date = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    workintro_id = Column(BIGINT(20), index=True, comment='工作简介ID 外键:t_work_introduction(id)')
    staff_id = Column(BIGINT(20), index=True, comment='人员ID 外键:t_staff(id)')
    business_unit_id = Column(ForeignKey('t_business_unit.id'), index=True, comment='部门ID 外键:t_business_unit(id)')
    json = Column(JSON, comment='JSON字段用于日报后续扩展开发')

    business_unit = relationship('TBusinessUnit')


class TDict(Base):
    __tablename__ = 't_dict'

    id = Column(BIGINT(64), primary_key=True, comment='字典ID:主键,自动增长')
    type_id = Column(ForeignKey('t_dict_type.id'), nullable=False, index=True, comment='FK(指向类型表id)')
    dict_code = Column(String(100, 'utf8_croatian_ci'), nullable=False, comment='字典名称Code')
    dict_value = Column(String(100, 'utf8_croatian_ci'), nullable=False, comment='字典值 通过dict_code字典值')
    remarks = Column(String(255, 'utf8_croatian_ci'), comment='备注')

    type = relationship('TDictType')


class TProFile(Base):
    __tablename__ = 't_pro_file'

    id = Column(BIGINT(20), primary_key=True)
    pro_code = Column(ForeignKey('t_project.id'), index=True, comment='外键:引用项目表t_project(id)')
    f_id = Column(ForeignKey('t_program_file.id'), index=True, comment='外键:引用程序文件表t_program_file(id)')

    f = relationship('TProgramFile')
    t_project = relationship('TProject')


class TConcernStaff(Base):
    __tablename__ = 't_concern_staff'

    id = Column(BIGINT(20), primary_key=True, comment='人员关注表主键:id,自动增长')
    concern_group = Column(String(255, 'utf8_croatian_ci'), nullable=False, comment='关注人员组')
    staff_id = Column(ForeignKey('t_staff.id'), nullable=False, index=True, comment='人员ID 外键:t_staff(id)')

    staff = relationship('TStaff')


t_t_on_business_daily_record = Table(
    't_on_business_daily_record', metadata,
    Column('id', BIGINT(20), comment='出差日报主键ID 自动增长'),
    Column('work_date', TIMESTAMP, comment='工作时间 注:当前日期 如:2018-11.29'),
    Column('start_date', TIMESTAMP, comment='开始时间 注:出差时间 如今天出差则:2018-11.29'),
    Column('weeks', BIGINT(20), comment='周 注:该年的第几周'),
    Column('staff_name', String(20, 'utf8_croatian_ci'), comment='人员姓名 注:方便查询'),
    Column('day_in_week', BIGINT(255), comment='星期几 注:一周七天 1,2,3,4,5,6,7'),
    Column('client_name', String(100, 'utf8_croatian_ci'), comment='客户姓名'),
    Column('on_business_place', String(20, 'utf8_croatian_ci'), comment='出差地点'),
    Column('project_id', String(50, 'utf8_croatian_ci'), comment='项目ID 外键:t_project_summary(id)'),
    Column('project_alias', String(255, 'utf8_croatian_ci'), comment='项目别名 注:主要用于方便查询!'),
    Column('work_matters', String(3500, 'utf8_croatian_ci'), comment='出差目的及每天工作的内容'),
    Column('new_demand', String(1000, 'utf8_croatian_ci'), comment='现场新增需求'),
    Column('matter_records', String(2000, 'utf8_croatian_ci'), comment='问题记录 注:主要记录出差时遇到的问题'),
    Column('staff_id', ForeignKey('t_staff.id'), index=True, comment='人员ID 外键:t_staff(id)'),
    Column('isdelete', BIGINT(11), comment='是否已删除 0:否 1:是'),
    Column('create_date', TIMESTAMP, comment='创建时间'),
    Column('update_date', TIMESTAMP, comment='更新时间 注:记录该数据什么时候被修改的'),
    Column('department', String(10, 'utf8_croatian_ci'), comment='部门名称'),
    Column('business_unit', String(20, 'utf8_croatian_ci'), comment='事业部 注:也就是父部门名称'),
    Column('json', JSON, comment='JSON字段用于出差日报后续扩展开发')
)


class TTempGroup(Base):
    __tablename__ = 't_temp_group'

    id = Column(BIGINT(20), primary_key=True, comment='临时组ID主键')
    create_date = Column(TIMESTAMP(fsp=6), nullable=False, server_default=text("CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)"), comment='创建时间')
    group_member = Column(String(255, 'utf8_croatian_ci'), comment='小组成员 注:存入的为人员表中的t_staff(id) 一组最多8人')
    manager_id = Column(ForeignKey('t_staff.id'), index=True, comment='组长ID 外键:t_satff(id)')
    remarks = Column(String(255, 'utf8_croatian_ci'), comment='备注')

    manager = relationship('TStaff')


