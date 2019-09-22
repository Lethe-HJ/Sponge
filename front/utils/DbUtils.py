from sqlalchemy.engine.result import ResultProxy, RowProxy
from sqlalchemy.ext.declarative import DeclarativeMeta
from flask_sqlalchemy import Pagination
from flask import abort, request, make_response, redirect, g
from front import db, sysdb
import time
import os
import csv
import codecs
import xlwt
import json
from front.models.rpt_header import RptHeader
from front.models.rpt_report import RptReport
import datetime
import re
from decimal import Decimal

#ref: http://docs.sqlalchemy.org/en/latest/core/metadata.html#sqlalchemy.schema.SchemaItem

#标题栏字段排序算法
def rpt_header_comp(header1, header2):
    if header1.ord != None and header1.ord < header2.ord:
        return -1

    return 1

def export_headers(sheet1, row):
    if not hasattr(g, 'rpt_headers'):
        g.rpt_headers = []

    items = row.items()
    for item in items:
        #字段名称
        name = item[0]

        #是否在字段配置表(g.rpt_headers)中已经存在
        exist = False

        for rpt_header in g.rpt_headers:
            if rpt_header.name == name:
                exist = True

        if not exist:
            rpt_header = RptHeader(
				name = name,
                title = name
			)

            g.rpt_headers.append(rpt_header)

    #标题栏字段排序
    g.rpt_headers.sort(rpt_header_comp)

    titles = []
    for item in g.rpt_headers:
        titles.append(item.title)

    #输出标题栏
    #CSV
    if hasattr(sheet1, 'writerow'):
        sheet1.writerow(titles)

    #XLS
    if isinstance(sheet1, xlwt.Worksheet):
        #合并居中分格
        font = xlwt.Font()
        font.height = 400

        style = xlwt.XFStyle()
        style.alignment.horz = xlwt.Alignment.HORZ_CENTER
        style.font = font

        r1 = r2 = 0
        c1 = 0
        c2 = len(titles) - 1
        sheet1.write_merge(r1, r2, c1, c2, g.rpt_report.title, style = style)

        for col in range(len(titles)):
            sheet1.write(1, col, titles[col])

    #分组字段
    g.grouped_cols = get_grouped_cols()

    #无分组，不需要合并单元格
    if len(g.grouped_cols) == 0:
        g.rpt_report.rowspan = 0

    #累加字段
    g.acc_cols = get_acc_cols()

#分组字段
def get_grouped_cols():
    grouped_cols = []

    for i in range(len(g.rpt_headers)):
        if g.rpt_headers[i].grouped == 1:
            grouped_cols.append(i)

    return grouped_cols

def get_acc_cols():
    acc_cols = []

    for i in range(len(g.rpt_headers)):
        if g.rpt_headers[i].acc == 1:
            acc_cols.append(i)

    return acc_cols

def acc(acc_row, current_row):
    for col in g.acc_cols:
        col_value = current_row[col]
        col_value = str(col_value)
        if col_value == None or col_value.strip() == '':
            pass
        else:
            acc_row[col] = acc_row[col] + Decimal(current_row[col])

    return acc_row

def acc_init(current_row):
    acc_row = []
    for col in range(len(g.rpt_headers)):
        if g.rpt_headers[col].acc:
            col_value = current_row[col]
            col_value = str(col_value)
            if col_value == None or col_value.strip() == '':
                acc_row.append(0)
            else:
                acc_row.append(Decimal(col_value))
        else:
            acc_row.append('')

    return acc_row

def export_csv(result):
    url = '/static/export/%s/%s.csv' % (time.strftime('%Y%m'), time.strftime('%Y%m%d-%H%M%S'))
    filename = 'front' + url
    export_dir, _ = os.path.split(filename)

    if not os.path.exists(export_dir):
        os.makedirs(export_dir)

    #写文件
    with codecs.open(filename,'wb',encoding='gb18030') as f:
        writer = csv.writer(f, dialect='excel')

        i = 0
        for row in result:
            if i == 0:
                #输出表头
                export_headers(writer, row)

            #输出内容
            current_row = []

            for header in g.rpt_headers:
                col = row[header.name]

                if col == None:
                    col = ''

                if isinstance(col, datetime.datetime):
                    if col.year >= 1900:
                        col = col.strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        col= '{0.year:04d}-{0.month:02d}-{0.day:02d} {0.hour:02d}:{0.minute:02d}:{0.second:02d}'.format(col) 

                #解决EXCEL中科学计算法显示数字的问题
                current_row.append(str(col) + '\t')

            #写CSV文件
            writer.writerow(current_row)

            #行号自增
            i = i + 1

        if i == 0:
            no_result = ['根据过滤条件，查找不到任何数据']
            writer.writerow(no_result)

    return redirect(url)

def writerow(sheet1, i, current_row):
    #报表抬头+字段抬头，共2行
    row = i + 2

    for col in range(len(current_row)):
        col_value = current_row[col]

        if isinstance(col_value, (Decimal)):
            col_value = '%.2f' % col_value
        else:
            col_value = str(col_value) + '\t';

        sheet1.write(row, col, col_value)

def export_xls(result):
    url = '/static/export/%s/%s.xls' % (time.strftime('%Y%m'), time.strftime('%Y%m%d-%H%M%S'))
    filename = 'front' + url
    export_dir, _ = os.path.split(filename)

    if not os.path.exists(export_dir):
        os.makedirs(export_dir)

    #写文件
    wbk = xlwt.Workbook(encoding='utf-8')
    sheet1 = wbk.add_sheet('sheet1', cell_overwrite_ok=True)

    #字体
    font = xlwt.Font()
    font.name = 'Calibri'   #Calibri
    font.height = 220       #11

    #设置默认字体
    xlwt.Style.default_style.font = font

    #合并居中分格
    style = xlwt.XFStyle()
    style.alignment.vert = xlwt.Alignment.VERT_CENTER
    style.font = font

    i = 0
    for row in result:
        #输出表头
        if i == 0:
            export_headers(sheet1, row)

        current_row = []

        for header in g.rpt_headers:
            col = row[header.name]

            if col == None:
                col = ''

            if isinstance(col, datetime.datetime):
                if col.year >= 1900:
                    col = col.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    col= '{0.year:04d}-{0.month:02d}-{0.day:02d} {0.hour:02d}:{0.minute:02d}:{0.second:02d}'.format(col) 

            current_row.append(col)

        #分组合并单元格
        if g.rpt_report.rowspan == 1:
            if i == 0:
                rowspan = [2] * len(current_row)
            else:
                for col in g.grouped_cols:
                    if current_row[col] != prev_row[col]:
                        r1 = rowspan[col]
                        r2 = i + 1
                        c1 = c2 = col
                        rowspan[col] = r2 + 1

                        if r2 - r1 > 1:
                            sheet1.write_merge(r1, r2, c1, c2, prev_row[col], style=style)

        #小计
        if len(g.grouped_cols) > 0:
            if i == 0:
                subtotal = acc_init(current_row)
            else:
                different = False

                for col in g.grouped_cols:
                    if current_row[col] != prev_row[col]:
                        different = True
                        break

                if different:
                    #切换分组，输出小计行，重新开始小计
                    subtotal[0] = '小计'
                    writerow(sheet1, i, subtotal)
                    subtotal = acc_init(current_row)

                    i = i + 1

                    if g.rpt_report.rowspan == 1:
                        for col in range(len(rowspan)):
                            rowspan[col] = i + 2
                else:
                    #小计
                    subtotal = acc(subtotal, current_row)
        
        #合计
        if g.rpt_report.acc_total == 1:
            if i == 0:
                total = acc_init(current_row)
            else:
                total = acc(total, current_row)

        prev_row = current_row

        writerow(sheet1, i, current_row)

        #行号自增
        i = i + 1

    #最后一个分组合并单元格
    if i > 0 and g.rpt_report.rowspan == 1:
        for col in g.grouped_cols:
            r1 = rowspan[col]
            r2 = i + 1
            c1 = c2 = col
            rowspan[col] = r2 + 1

            if r2 - r1 > 1:
                sheet1.write_merge(r1, r2, c1, c2, prev_row[col], style=style)

    #最后一个小计
    if i > 0 and len(g.grouped_cols) > 0:
        subtotal[0] = '小计'
        writerow(sheet1, i, subtotal)
        i = i + 1

    #输出合计
    if i > 0 and g.rpt_report.acc_total == 1:
        total[0] = '合计'
        writerow(sheet1, i , total)

    if i == 0:
        sheet1.write(0, 0, '根据过滤条件，查找不到任何数据')

    wbk.save(filename)

    return redirect(url)

def to_dict(row):
    obj = {}

    for i in range(len(g.rpt_headers)):
        name = g.rpt_headers[i].name
        col_value = row[i]
        
        if isinstance(col_value, (Decimal)):
            col_value = '%.2f' % col_value
        else:
            col_value = str(col_value);

        obj[name] = col_value

    return obj

def post_process(result):
    #结果集
    items = []

    i = 0
    for row in result:
        if i == 0:
            export_headers(None, row)

        current_row = []

        for header in g.rpt_headers:
            col = row[header.name]

            if col == None:
                col = ''

            if isinstance(col, datetime.datetime):
                if col.year >= 1900:
                    col = col.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    col= '{0.year:04d}-{0.month:02d}-{0.day:02d} {0.hour:02d}:{0.minute:02d}:{0.second:02d}'.format(col) 

            current_row.append(col)

        #小计
        if len(g.grouped_cols) > 0:
            if i == 0:
                subtotal = acc_init(current_row)
            else:
                different = False

                for col in g.grouped_cols:
                    if current_row[col] != prev_row[col]:
                        different = True
                        break

                if different:
                    #切换分组，输出小计行，重新开始小计
                    subtotal[0] = '小计'
                    items.append(to_dict(subtotal))
                    subtotal = acc_init(current_row)

                    i = i + 1
                else:
                    #小计
                    subtotal = acc(subtotal, current_row)
        
        #合计
        if g.rpt_report.acc_total == 1:
            if i == 0:
                total = acc_init(current_row)
            else:
                total = acc(total, current_row)

        prev_row = current_row

        items.append(to_dict(current_row))

        #行号自增
        i = i + 1

    #最后一个小计
    if i > 0 and len(g.grouped_cols) > 0:
        subtotal[0] = '小计'
        items.append(to_dict(subtotal))
        i = i + 1

    #输出合计
    if i > 0 and  g.rpt_report.acc_total == 1:
        total[0] = '合计'
        items.append(to_dict(total))

    return items

def toList(result):
    if isinstance(result, ResultProxy):
        return result.fetchall()

    if isinstance(result, Pagination):
        dict = {}
        dict["has_next"] = result.has_next
        dict["has_prev"] = result.has_prev
        dict["next_num"] = result.next_num
        dict["prev_num"] = result.prev_num
        dict["page"] = result.page
        dict["pages"] = result.pages
        dict["per_page"] = result.per_page
        dict["total"] = result.total

        items = []
        for item in result.items:
            items.append(item)
        dict["items"] = items

        return dict
    
    abort(404, '记录不存在')

def toDict(result):
    #SqlAlchemy表转dict
    if isinstance(result.__class__, DeclarativeMeta):
        return {c.name: getattr(result, c.name, None) for c in result.__table__.columns}

    if isinstance(result, ResultProxy):
        list = result.fetchall()

        #找不到记录
        if len(list) == 0:
            abort(404)

        row = list[0]

        fields = {}
        for item in row.items():
            fields[item[0]] = item[1]
        return fields

    if isinstance(result, RowProxy):
        row = result

        fields = {}
        for item in row.items():
            fields[item[0]] = item[1]
        return fields

    abort(404, '记录不存在')

def paginate(sql, order_by, database=db, params=[]):
    if not hasattr(g, 'rpt_report'):
        g.rpt_report = RptReport(
            sql = sql,
            order_by = order_by,
            paging = 1
        )

    if not hasattr(g, 'rpt_headers'):
        g.rpt_headers = []

    if request:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
    else:
        page = 1
        per_page = 20

    #是否分页
    if g.rpt_report.paging == 1 and request.args.get('export') == None and per_page != 0:
        paging = 1
    else:
        paging = 0

    #SELECT语句
    if re.search(r'^select\b', sql, re.IGNORECASE) != None:
        #默认MSSQL数据库
        count_sql = "select count(*) as count from (%s) anon_1" % (sql)
        items_sql = 'select * from (select ROW_NUMBER() OVER (ORDER BY %s) AS rownumber, %s) anon_1 where rownumber > %s and rownumber <= %s' % (order_by, sql[7:], (page - 1) * per_page, page * per_page)
    
        #MYSQL数据库
        if database.session.bind.name == 'mysql':
            count_sql = "select count(*) as count from (%s) anon_1" % (sql)
            items_sql = '%s order by %s limit %s, %s' % (sql, order_by, (page - 1) * per_page, per_page)

        #oracle数据库
        if database.session.bind.name == 'oracle':
            count_sql = "select count(*) as count from (%s) anon_1" % (sql)
            items_sql = 'SELECT * FROM (SELECT tt.*, ROWNUM AS rownumber FROM ( %s ORDER BY %s) tt) anon_1 where rownumber > %s and rownumber <= %s' % (sql, order_by, (page - 1) * per_page, page * per_page)
        

        #总记录条数
        result = database.session.execute(count_sql).fetchone()
        count = result['count']

        #不分页
        if paging == 0:
            items_sql = sql

        #记录集
        result = database.session.execute(items_sql)

    #存储过程
    if re.search(r'^exec\b', sql, re.IGNORECASE) != None:
        #存储过程分页
        params.append('@page = %d' % page)
        params.append('@per_page = %d' % per_page)
        params.append('@paging = %s' % paging)

        sql = "%s %s" % (sql, ', '.join(params))

        #执行存储过程
        rp = database.session.execute(sql)
        
        #第一个结果集: 记录总数
        count = rp.cursor.fetchone()
        count = count[0]
        
        if not rp.cursor.nextset():
            return abort(404, '存储过程返回的结果集数量错') 

        #重新初始化meta
        rp._init_metadata()

        #第二个结果集: 分页后的数据
        result = rp

    #ORACLE 存储过程
    #ref: https://stackoverflow.com/questions/8390212/executing-an-oracle-stored-procedure-returning-a-ref-cursor-using-sqlalchemy
    if re.search(r'^call\b', sql, re.IGNORECASE) != None:
        proc_name = sql[5:]
        #---------------------------------------------
        conn = database.engine.raw_connection()
        cursor = conn.cursor()
        pageResultSet = conn.cursor()

        params.insert(0, 0)
        params.insert(1, pageResultSet)
        params.insert(2, page)
        params.insert(3, per_page)
        params.insert(4, paging)

        result = cursor.callproc(proc_name, params)

        count = result[0]

        names = []
        for description in pageResultSet.description:
            names.append(description[0])

        result = []
        while True:
            row = pageResultSet.fetchone()
            if row is None:
                break
            obj = {}
            for i in range(len(names)):
                name = names[i]
                obj[name] = row[i]
            result.append(obj)

        cursor.close()
        pageResultSet.close()
        #---------------------------------------------

    #导出
    if request.args.get('export') == 'csv':
        return export_csv(result)

    if request.args.get('export') == 'xls':
        return export_xls(result)

    #页面小计、合计
    items = post_process(result)

    if paging == 0:
        count = len(items)

    p = Pagination(None, page, per_page, count, items)

    result = {}
    result["has_next"] = p.has_next
    result["has_prev"] = p.has_prev
    result["next_num"] = p.next_num
    result["prev_num"] = p.prev_num
    result["page"] = p.page
    result["pages"] = p.pages
    result["per_page"] = p.per_page
    result["total"] = p.total
    result["items"] = items

    return result
