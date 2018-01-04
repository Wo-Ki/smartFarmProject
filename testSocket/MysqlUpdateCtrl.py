# coding:utf-8
# /usr/bin/python

# creator = wangkai
# creation time = 2017/12/25 20:11

from MySQLdb import *
from datetime import datetime


class MysqlUpdateCtrl(object):
    def __init__(self, host, db, user, passwd, port=3306, charset="utf8"):
        self.host = host
        self.port = port
        self.db = db
        self.user = user
        self.passwd = passwd
        self.charset = charset

        self.open()

    def open(self):
        self.conn = connect(host=self.host, port=self.port, db=self.db, user=self.user, passwd=self.passwd,
                            charset=self.charset)
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def cud(self, sql, params=()):
        try:
            # self.open()
            self.cursor.execute(sql, params)
            self.conn.commit()
            # print "OK"
            # self.close()
        except Exception, e:
            print e.message

    def all(self, sql):
        try:
            # self.open()
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            # self.close()
            return result
        except Exception, e:
            print e.message

    def one(self, sql, params=()):
        try:
            # self.open()
            self.cursor.execute(sql, params)
            result = self.cursor.fetchone()
            # self.close()
            return result
        except Exception, e:
            print e.message


if __name__ == "__main__":
    sqlCtrl = MysqlUpdateCtrl("192.168.100.3", "smartFarmTest", "root", "123456")

    # k = {"deviceID": 2, "status": 2}
    # # sql = "update devicesTable set status=1,changeTime=%s where deviceID = %s"
    # sql2 = "insert into {} values (%s,%s,%s)".format("devicesTable")
    # print sql2
    # sqlCtrl.cud(sql2, ("1006", -1, datetime.now()))

    # sql = "desc %s" % ("data1001Table")
    # print [x[0] for x in sqlCtrl.all(sql)]

    # jsonData = {'temIn': 23.4, 'M': 'update', 'ID': '1001', 'humIn': 41.5, "temOut": "32.3", "temIn": 21}
    # sqlTitles = "desc %s" % ("data" + str(jsonData["ID"]) + "Table")
    # tableTitles = [x[0] for x in sqlCtrl.all(sqlTitles)]
    # print tableTitles
    # sql = "insert into %s (" % ("data" + str(jsonData["ID"]) + "Table",)
    # values = []
    # for i in jsonData.keys():
    #     if i in tableTitles:
    #         sql += str(i) + ","
    #         values.append(jsonData[i])
    # values.append(jsonData["ID"])
    # # values.append(str(datetime.now()))
    # print values
    # sql += "deviceID,create_time"
    # sql += ") values ("
    # for i in values:
    #     sql += str(i) + ","
    # # sql = sql[0:-1]
    # sql += "%s)"
    # # sql = sql % (datetime.now())
    # print sql
    # sqlCtrl.cud(sql, (datetime.now(),))
    jsonData = {'ID': '1001', 'col1': "water1_1", 'M': 'status', 'col2': "temCtrl1_1", "col3": "windCtrl_1"}
    sql = "select status from devicesTable where ID = %s"
    # if str(sqlCtrl.one(sql, (jsonData["ID"],))[0]) == "0":
    #     print "devicesJsonData status: off line!!!"

    sql = "select * from statusTable where ID = %s"
    sqlTitles = "desc statusTable"
    tableTitles = [x[0] for x in sqlCtrl.all(sqlTitles)]
    print tableTitles
    if sqlCtrl.one(sql, (jsonData["ID"],)) is None:

        values = []
        sql = "insert into statusTable ("
        for i in jsonData.keys():
            if i in tableTitles:
                sql += str(i) + ","
                values.append(jsonData[i])
        print values
        sql += "changeTime) values ("

        for i in values:
            sql += "\"" + str(i) + "\"" + ","

        sql += "%s)"
        print(sql)
        sqlCtrl.cud(sql, (datetime.now(),))
    else:
        sql = "update statusTable set "
        for i in jsonData.keys():
            if i in tableTitles:
                sql += str(i) + "=\"" + str(jsonData[i]) + "\","

        # sql = sql[0:-1]
        sql += " changeTime=%s where ID = %s"
        print sql
        sqlCtrl.cud(sql, (datetime.now(), jsonData["ID"]))

    sqlCtrl.close()
