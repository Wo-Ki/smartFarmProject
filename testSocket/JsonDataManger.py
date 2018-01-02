# coding:utf-8
# /usr/bin/python

# creator = wangkai
# creation time = 2017/12/25 20:37
from datetime import datetime
import time


class JsonDataManager(object):
    @staticmethod
    def devicesJsonData(jsonData, clientSocket, clientAddress):
        global deviceSockets, sqlCtrl, lock
        """处理设备的json数据"""
        if jsonData["M"] == "checkin":
            sql = "select * from devicesTable where deviceID = %s"
            if sqlCtrl.one(sql, jsonData["ID"]) is not None:
                # 如果数据库中有改设备，更改status为1
                sql = "update devicesTable set status=1,changeTime=%s where deviceID = %s"
                sqlCtrl.cud(sql, (datetime.now(), jsonData["ID"]))
            else:
                sql = "insert into devicesTable (deviceID, status, changeTime) values (%s,%s,%s)"
                sqlCtrl.cud(sql, (jsonData["ID"], 1, datetime.now()))
            backData = """{"M":"checkinok","ID":"{}","T":"{}"}\n""".format(jsonData["ID"], time.time())
            clientSocket.send(bytes(backData))
        elif jsonData["M"] == "update":
            sql1 = "select * from devicesTable where deviceID = %s"
            sql2 = "select status from devicesTable where deviceID = %s"
            if sqlCtrl.one(sql1, jsonData["ID"]) is None:
                backData = """{"M":"Error","ID":"{}","K":"{}"}\n""".format(jsonData["ID"], "Not Found")
                clientSocket.send(bytes(backData))
                return
            elif str(sqlCtrl.one(sql2, jsonData["ID"])) == "0":
                backData = """{"M":"Error","ID":"{}","K":"{}"}\n""".format(jsonData["ID"], "Off Line")
                clientSocket.send(bytes(backData))
                return
            else:
                sql = "insert into %s (deviceID,temValue, humValue, windCtrl, temCtrl, create_time) values (%s,%s,%s,%s,%s,%s)"
                sqlCtrl.cud(sql, (
                    "data" + str(jsonData["ID"]) + "Table", jsonData["ID"], jsonData["tem"], jsonData["hum"],
                    jsonData.get("windCtrl"), jsonData.get("temCtrl"), datetime.now()))
        elif jsonData["M"] == "say":
            try:
                sourceID = list(deviceSockets.keys())[list(deviceSockets.values()).index(clientSocket)]
                targetData = """{"M":"say","ID":"{}","C":"{}","T":"{}"}\n""".format(sourceID, jsonData.get("C"),
                                                                                    time.time())
                deviceSockets.get(jsonData.get("ID")).send(bytes(targetData))
                clientSocket.send(bytes("""{"M":"Send Success"}\n"""))
                # 将通知信息存到数据库notificationTable
                sql = "insert into notificationTable (sourceID,targetID,message) values (%s,%s,%s,%s)"
                sqlCtrl.cud(sql, (sourceID, jsonData.get("ID"), jsonData.get("C"), time.time()))
            except:
                print """{"M":"Send Error"}"""
                clientSocket.send(bytes("""{"M":"Send Error"}\n"""))

        elif jsonData["M"] == "isOL":
            tLists = jsonData["ID"]
            onDicts = {}
            for tList in tLists:
                sql = "select status from devicesTable where deviceID = %s"
                if deviceSockets.get(tList) is not None and str(sqlCtrl.one(sql, (tList))) == "1":
                    # 说明设备在线
                    onDicts[tList] = "1"
                else:
                    onDicts[tList] = "0"
            sendData = """{"M":"isOL","R":{},"T":"{}"}\n""".format(str(onDicts), time.time())
            clientSocket.send(bytes(sendData))
        elif jsonData["M"] == "status":
            sourceID = list(deviceSockets.keys())[list(deviceSockets.values()).index(clientSocket)]
            sql = "select status from devicesTable where deviceID = %s"
            status = sqlCtrl.one(sql, (sourceID,))
            clientSocket.send(bytes("""{"M":"{}"}\n""".format(str(status))))
        elif jsonData["M"] == "alert":
            alertData = jsonData["C"]
            sourceID = list(deviceSockets.keys())[list(deviceSockets.values()).index(clientSocket)]
            sql = "insert into alertTable (deviceID, message, create_time) values (%s,%s,%s)"
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
            targetID = jsonData["ID"]
            sql = "select status from devicesTable where deviceID = %s"
            if deviceSockets.get(targetID) is None and str(sqlCtrl.one(sql, (targetID))) == "0":
                sendData = """{"M":"Already OffLine"}"""
                clientSocket.send(bytes(sendData))
                return
            targetData = """{"M":"checkout","IP":"{}","T":"{}"}\n""".format(str(clientAddress), time.time())
            deviceSockets.get(targetID).send(bytes(targetData))
            sql = "update devicesTable set status=0 where deviceID = %s"
            sqlCtrl.cud(sql, (targetID,))
            if lock.acquire():
                deviceSockets.pop(targetID)
                lock.release()


    @staticmethod
    def flaskJsonData(jsonData):
        """处理flask的json数据"""
        global device_sockets
        if jsonData["M"] == "say":
            pass
        elif jsonData["M"] == "checkout":
            pass
