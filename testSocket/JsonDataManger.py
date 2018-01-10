# coding:utf-8
# /usr/bin/python

# creator = wangkai
# creation time = 2017/12/25 20:37
from datetime import datetime
import time
from MysqlUpdateCtrl import MysqlUpdateCtrl


class JsonDataManager(object):
    # def __init__(self):
    #     self.sqlCtrl = MysqlUpdateCtrl("192.168.100.3", "smartFarmTest", "root", "123456")

    @staticmethod
    def devicesJsonData(jsonData, clientSocket, sqlCtrl, deviceSockets):
        """处理设备的json数据"""

        # global deviceSockets
        global lock
        # global deviceSockets
        # print "devicesJsonData:", jsonData
        if jsonData["M"] == "checkin":
            sql = "select * from devicesTable where ID = %s"
            if sqlCtrl.one(sql, (jsonData["ID"],)) is not None:
                # 如果数据库中有改设备，更改status为1
                sql = "update devicesTable set status=1,changeTime=%s where ID = %s"
                sqlCtrl.cud(sql, (datetime.now(), jsonData["ID"]))
            else:
                sql = "insert into devicesTable (ID, status, changeTime) values (%s,%s,%s)"
                sqlCtrl.cud(sql, (jsonData["ID"], 1, datetime.now()))
            backData = """{"M":"checkinok","ID":"{}","T":"{}"}\n""".format(jsonData["ID"], time.time())
            clientSocket.send(bytes(backData))
        elif jsonData["M"] == "update":
            sql1 = "select * from devicesTable where ID = %s"
            sql2 = "select status from devicesTable where ID = %s"
            if sqlCtrl.one(sql1, (jsonData["ID"],)) is None:
                backData = """{"M":"Error","ID":"{}","K":"{}"}\n""".format(jsonData["ID"], "Not Found")
                clientSocket.send(bytes(backData))
                return
            elif str(sqlCtrl.one(sql2, (jsonData["ID"],))) == "0":
                backData = """{"M":"Error","ID":"{}","K":"{}"}\n""".format(jsonData["ID"], "Off Line")
                clientSocket.send(bytes(backData))
                return
            else:
                sqlTitles = "desc %s" % ("data" + str(jsonData["ID"]) + "Table")
                tableTitles = [x[0] for x in sqlCtrl.all(sqlTitles)]
                # print tableTitles
                sql = "insert into %s (" % ("data" + str(jsonData["ID"]) + "Table",)
                values = []
                for i in jsonData.keys():
                    if i in tableTitles:
                        sql += str(i) + ","
                        values.append(jsonData[i])
                # print values
                sql += "create_time"
                sql += ") values ("
                for i in values:
                    sql += str(i) + ","
                # sql = sql[0:-1]
                sql += "%s)"
                # sql = sql % (datetime.now())
                # print sql
                sqlCtrl.cud(sql, (datetime.now(),))
        elif jsonData["M"] == "say":
            try:
                sourceID = list(deviceSockets.keys())[list(deviceSockets.values()).index(clientSocket)]
                targetData = """{"M":"say","SID":"{}","C":"{}","T":"{}"}\n""".format(sourceID, jsonData.get("C"),
                                                                                     time.time())
                deviceSockets.get(jsonData.get("ID")).send(bytes(targetData))
                clientSocket.send(bytes("""{"M":"Send Success"}\n"""))
                # 将通知信息存到数据库notificationTable
                sql = "insert into notificationTable (SID,TID,message) values (%s,%s,%s,%s)"
                sqlCtrl.cud(sql, (sourceID, jsonData.get("ID"), jsonData.get("C"), time.time()))
            except:
                print """{"M":"Send Error"}"""
                clientSocket.send(bytes("""{"M":"Send Error"}\n"""))

        elif jsonData["M"] == "isOL":
            tLists = jsonData["TID"]
            onDicts = {}
            for tList in tLists:
                sql = "select status from devicesTable where ID = %s"
                if deviceSockets.get(tList) is not None and str(sqlCtrl.one(sql, (tList))) == "1":
                    # 说明设备在线
                    onDicts[tList] = "1"
                else:
                    onDicts[tList] = "0"
            sendData = """{"M":"isOL","R":{},"T":"{}"}\n""".format(str(onDicts), time.time())
            clientSocket.send(bytes(sendData))
        elif jsonData["M"] == "status":
            print "status data:", jsonData
            sql = "select status from devicesTable where ID = %s"
            if deviceSockets.get(jsonData["ID"]) is None and str(sqlCtrl.one(sql, (jsonData["ID"]))) == "0":
                print "devicesJsonData status: off line!!!"
                clientSocket.send(bytes("""{"M":"Error!"}\n"""))
                return
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

                sql += " changeTime=%s where ID = %s"
                print "status sql:", sql
                sqlCtrl.cud(sql, (datetime.now(), jsonData["ID"]))
            clientSocket.send(bytes("""{"M":"OK"}\n"""))
        elif jsonData["M"] == "alert":
            alertData = jsonData["C"]
            sourceID = list(deviceSockets.keys())[list(deviceSockets.values()).index(clientSocket)]
            sql = "insert into alertTable (ID, message, create_time) values (%s,%s,%s)"
            sqlCtrl.cud(sql, (sourceID, str(alertData), datetime.now()))
        elif jsonData["M"] == "time":
            f = jsonData["F"]
            if f == "stamp":
                sendData = str(time.time())
            elif f == "Y-m-d":
                sendData = datetime.datetime.now().strftime("%Y-%m-%d")
            elif f == "Y.m.d":
                sendData = datetime.datetime.now().strftime("%Y.%m.%d")
            elif f == "Y-m-d H:i:s":
                sendData = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            else:
                sendData = "Error"
            clientSocket.send(bytes("""{"M":"time","T":"{}"}\n""".format(sendData)))
        elif jsonData["M"] == "checkout":
            targetID = jsonData["TID"]
            sql = "select status from devicesTable where ID = %s"
            if deviceSockets.get(targetID) is None and str(sqlCtrl.one(sql, (targetID))) == "0":
                sendData = """{"M":"Already OffLine"}\n"""
                clientSocket.send(bytes(sendData))
                return
            sendData = """{"M":"OK"}\n"""
            clientSocket.send(bytes(sendData))
            sourceID = list(deviceSockets.keys())[list(deviceSockets.values()).index(clientSocket)]
            targetData = """{"M":"checkout","SID":"{}","T":"{}"}\n""".format(str(sourceID), time.time())
            deviceSockets.get(targetID).send(bytes(targetData))
            sql = "update devicesTable set status=0 where ID = %s"
            sqlCtrl.cud(sql, (targetID,))
            if lock.acquire():
                deviceSockets.pop(targetID)
                lock.release()

    @staticmethod
    def flaskJsonData(jsonData, clientAddress, sqlCtrl, deviceSockets):
        """处理flask的json数据"""
        # global deviceSockets
        print "flaskJsonData", jsonData
        if jsonData["M"] == "say":
            targetID = jsonData["ID"]
            sql = "select status from devicesTable where ID = %s"
            # print "targetID:", targetID
            # print "deviceSockets:", deviceSockets
            # print "str(sqlCtrl.one(sql, (targetID,)))", str(sqlCtrl.one(sql, (targetID,))[0])
            if deviceSockets.get(targetID) is None or str(sqlCtrl.one(sql, (targetID,))[0]) == "0":
                print("flaskJsonData:device off line")
                return
            deviceSockets[targetID].send(bytes(jsonData["C"]))
        elif jsonData["M"] == "checkout":
            targetID = jsonData["TID"]
            sql = "select status from devicesTable where deviceID = %s"
            if deviceSockets.get(targetID) is None or str(sqlCtrl.one(sql, (targetID,))[0]) == "0":
                print("flaskJsonData:Already OffLine")
                # sendData = """{"M":"Already OffLine"}\n"""
                # clientSocket.send(bytes(sendData))
                return
            # sendData = """{"M":"OK"}\n"""
            # clientSocket.send(bytes(sendData))

            targetData = """{"M":"checkout","IP":"{}","T":"{}"}\n""".format(str(clientAddress), time.time())
            deviceSockets.get(targetID).send(bytes(targetData))
            sql = "update devicesTable set status=0 where deviceID = %s"
            sqlCtrl.cud(sql, (targetID,))
            if lock.acquire():
                deviceSockets.pop(targetID)
                lock.release()

    @staticmethod
    def k(value):
        if value is None:
            return -1
        return value
