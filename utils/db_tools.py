# -*- coding: utf-8 -*-
import pymysql
import re,xlwt


DBCONFIG = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'passwd': 'Cyg123456',
        'dbname': 'vcar_vcyber_com',
        'charset': 'utf8mb4'
    }

class mysql(object):
    """docstring for mysql"""

    def __init__(self, dbconfig):
        self.host = dbconfig['host']
        self.port = dbconfig['port']
        self.user = dbconfig['user']
        self.passwd = dbconfig['passwd']
        self.dbname = dbconfig['dbname']
        self.charset = dbconfig['charset']
        self._conn = None
        self._connect()
        self._cursor = self._conn.cursor(pymysql.cursors.DictCursor)

    def _connect(self):
        try:
            self._conn = pymysql.connect(host=self.host,
                                         port=self.port,
                                         user=self.user,
                                         passwd=self.passwd,
                                         db=self.dbname,
                                         charset=self.charset)
        except Exception as e:
            print(e)

    def __del__(self):
        try:
            self._cursor.close()
            self._conn.close()
        except:
            pass

    def close(self):
        self.__del__()

    def query(self,sql):
        try:

            result = self._cursor.execute(sql)
        except Exception as e:
            result = False
        return result

    def rollback(self):
        self._conn.rollback()

    def affected_num(self):
        affected_num =self._cursor.rowcount
        self.close()
        return affected_num


def query(sql):
    try:
        db = mysql(DBCONFIG)
        result = db._cursor.execute(sql)
        db.close()
    except Exception as e:
        result = e
    return result


def select(table, column='*', condition=''):
    '''
    :param table: 表名
    :param column: 列名
    :param condition: 条件 column=？
    :return:
    '''

    condition = ' where ' + condition if condition else None
    if condition:
        sql = "select %s from %s %s" % (column, table, condition)
    else:
        sql = "select %s from %s" % (column, table)
    db = mysql(DBCONFIG)
    db.query(sql)
    #print(sql)
    result = db._cursor.fetchall()
    db.close()
    return result

def insert( table, tdict):
    '''
    :param table: 表名
    :param tdict: 列名与值的字典
    :return:
    '''
    column = ''
    value = ''
    for key in tdict:
        column += '`,`' + key
        value += "','" + tdict[key]
    column = column[2:]+"`"
    value = value[2:] + "'"
    sql = "insert into %s(%s) values(%s)" % (table, column, value)
    #print(sql)
    db = mysql(DBCONFIG)
    db._cursor.execute(sql)
    db._conn.commit()
    lastrowid = db._cursor.lastrowid  # 返回最后的id
    db.close()
    return lastrowid

def update(table, tdict, condition=''):
    if not condition:
        print("must have id")
        exit()
    else:
        condition = 'where ' + condition
    value = ''
    for key in tdict:
        value += ",`%s`='%s'" % (key, tdict[key])
    value = value[1:]
    sql = "update %s set %s %s;" % (table, value, condition)
    #print(sql)
    db = mysql(DBCONFIG)
    db._cursor.execute(sql)
    db._conn.commit()
    db.close()
    return db.affected_num()  # 返回受影响行数

def delete( table, condition=''):
    condition = 'where ' + condition if condition else None
    sql = "delete from %s %s" % (table, condition)
    # print sql
    db = mysql(DBCONFIG)
    db._cursor.execute(sql)
    db._conn.commit()
    db.close()
    return db.affected_num()  # 返回受影响行数

def table_exists( table_name):
    sql = "show tables;"
    db = mysql(DBCONFIG)
    db._cursor.execute(sql)
    tables = [db._cursor.fetchall()]
    table_list = re.findall('(\'.*?\')', str(tables))
    table_list = [re.sub("'", '', each) for each in table_list]
    if table_name in table_list:
        db.close()
        return True
    else:
        db.close()
        return False

def getColumn(tablename):
    conn = pymysql.connect(host="127.0.0.1",user="root",password="Cyg123456",db="mysql",autocommit=True)
    cur = conn.cursor()
    sql = "select COLUMN_NAME from information_schema.COLUMNS where table_name = '"+tablename+"';"
    cur.execute(sql)
    fields = []
    for field in cur.fetchall():
        field = "".join(field)
        fields.append(field)
    cur.close()
    conn.close()
    return fields

def dbexcute(sql):
    conn = pymysql.connect(host= DBCONFIG['host'], user=DBCONFIG['user'], password=DBCONFIG['passwd'], db=DBCONFIG['dbname'], autocommit=True)
    cur = conn.cursor()
    cur.execute(sql)
    cur.close()
    conn.close()

#每次存储前先判断记录是否存在
def is_exist(kv,tablename):
    value = ''
    for key in kv:
        value += key+"='" + kv[key]+"' and "
    result = select(tablename,"*",value[:-4])
    if result:
        return True
    else:
        return False


def export_excel(path,table_name):
    # 连接数据库，查询数据
    conn = pymysql.connect(host=DBCONFIG['host'], user=DBCONFIG['user'], password=DBCONFIG['passwd'],
                           db=DBCONFIG['dbname'], autocommit=True)
    cur = conn.cursor()
    sql = 'select * from %s' % table_name
    cur.execute(sql)  # 返回受影响的行数
    fields = [field[0] for field in cur.description]  # 获取所有字段名
    all_data = cur.fetchall()  # 所有数据

    # 写入excel
    book = xlwt.Workbook()
    sheet = book.add_sheet('sheet1')

    for col, field in enumerate(fields):
        sheet.write(0, col, field)

    row = 1
    for data in all_data:
        for col, field in enumerate(data):
            sheet.write(row, col, field)
        row += 1
    book.save("{}/{}.xls".format(path,table_name))

