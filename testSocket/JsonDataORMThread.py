# coding:utf-8
# /usr/bin/python

# creator = wangkai
# creation time = 2018/1/20 14:34

from datetime import datetime
import time
from models import DevicesTable, DataChenTable, NotificationTable, AlertTable, LogTable, StatusTable, GreenHouseImages
from exts import Base, session


class JsonDataORMCtrl(object):
    @staticmethod
    def devicesJsonData(jsonData, clientSocket, deviceSockets, lock):
        """处理设备的json数据"""
        # print "JsonData devices:", jsonData
        if jsonData["M"] == 'checkin':
            ID = jsonData.get('ID')
            if session.query(DevicesTable.ID).filter_by(ID=ID).first() is not None:
                # 如果数据库中有改设备，更改status为1
                session.query(DevicesTable).filter_by(ID=ID).update({"status": 1})
                session.commit()
            else:
                # 没有该设备则添加
                device = DevicesTable(ID=ID, status=1)
                session.add(device)
                session.commit()
                backData = """{"M":"checkinok","ID":"{}","T":"{}"}\n""".format(jsonData["ID"], time.time())
                clientSocket.send(bytes(backData))
        elif jsonData["M"] == 'update':
            ID = jsonData.get('ID')
            find = session.query(DevicesTable).filter_by(ID=ID).first()
            if find is None:
                backData = """{"M":"Error","ID":"{}","K":"{}"}\n""".format(jsonData["ID"], "Not Found")
                clientSocket.send(bytes(backData))
                return
            elif find.status == 0:
                backData = """{"M":"Error","ID":"{}","K":"{}"}\n""".format(jsonData["ID"], "Off Line")
                clientSocket.send(bytes(backData))
                return
            else:
                jsonData.pop("M")
                updateData = DataChenTable(**jsonData)
                session.add(updateData)
                session.commit()
        elif jsonData["M"] == "say":
            try:
                sourceID = list(deviceSockets.keys())[list(deviceSockets.values()).index(clientSocket)]
                targetData = """{"M":"say","SID":"{}","C":"{}","T":"{}"}\n""".format(sourceID, jsonData.get("C"),
                                                                                     time.time())
                deviceSockets.get(jsonData.get("TID")).send(bytes(targetData))
                clientSocket.send(bytes("""{"M":"Send Success"}\n"""))
                # 将通知信息存到数据库notificationTable
                jsonData.pop("M")
                updateData = jsonData
                updateData["SID"] = sourceID
                session.add(NotificationTable(**updateData))
                session.commit()
            except:
                pass
        elif jsonData["M"] == 'isOL':
            tLists = jsonData.get("TID")
            onDicts = {}
            for tID in tLists:
                find = session.query(DevicesTable.status).filter_by(ID=tID).first()
                if find == 1:
                    onDicts[tID] = '1'
                else:
                    onDicts[tID] = '0'
            sendData = """{"M":"isOL","R":{},"T":"{}"}\n""".format(str(onDicts), time.time())
            clientSocket.send(bytes(sendData))
        elif jsonData["M"] == "status":
            ID = jsonData.get('ID')
            find = session.query(DevicesTable).filter_by(ID=ID).first()
            if find is None:
                backData = """{"M":"Error","ID":"{}","K":"{}"}\n""".format(jsonData["ID"], "Not Found")
                clientSocket.send(bytes(backData))
                return
            elif find.status == 0:
                backData = """{"M":"Error","ID":"{}","K":"{}"}\n""".format(jsonData["ID"], "Off Line")
                clientSocket.send(bytes(backData))
                return
            else:
                find = session.query(StatusTable).filter_by(ID=ID).first()

                if find is None:
                    jsonData.pop("M")
                    new = StatusTable(**jsonData)
                    session.add(new)
                    session.commit()
                else:
                    jsonData.pop("M")
                    jsonData.pop("ID")
                    updateData = jsonData
                    updateData["changeTime"] = datetime.now()
                    session.query(StatusTable).filter_by(ID=ID).update(updateData)
                    session.commit()
                    clientSocket.send(bytes("""{"M":"OK"}\n"""))
        elif jsonData["M"] == "alert":
            sourceID = list(deviceSockets.keys())[list(deviceSockets.values()).index(clientSocket)]
            updateData = {"ID": sourceID, "message": jsonData.get("C")}
            session.add(AlertTable(**updateData))
            session.commit()
        elif jsonData["M"] == "time":
            f = jsonData["F"]
            if f == "stamp":
                sendData = str(time.time())
            elif f == "Y-m-d":
                sendData = datetime.now().strftime("%Y-%m-%d")
            elif f == "Y.m.d":
                sendData = datetime.now().strftime("%Y.%m.%d")
            elif f == "Y-m-d H:i:s":
                sendData = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            else:
                sendData = "Error"
            clientSocket.send(bytes("""{"M":"time","T":"{}"}\n""".format(sendData)))
        elif jsonData["M"] == "checkout":
            targetID = jsonData["TID"]
            find = session.query(DevicesTable).filter_by(ID=targetID).first()
            if find is None or find.status == 0:
                print("deviceJsonData:device off line")
                sendData = """{"M":"Already OffLine"}\n"""
                clientSocket.send(bytes(sendData))
                return
            sendData = """{"M":"OK"}\n"""
            clientSocket.send(bytes(sendData))
            sourceID = list(deviceSockets.keys())[list(deviceSockets.values()).index(clientSocket)]
            targetData = """{"M":"checkout","SID":"{}","T":"{}"}\n""".format(str(sourceID), time.time())
            deviceSockets.get(targetID).send(bytes(targetData))
            session.query(DevicesTable).filter_by(ID=targetData).update({"status": 0})
            session.commit()
            if lock.acquire():
                deviceSockets.pop(targetID)
                lock.release()
        else:
            clientSocket.send(bytes("""{"M":"Error","C":"No Such M"}\n"""))

    @staticmethod
    def flaskJsonData(jsonData, clientAddress, deviceSockets, lock):
        """处理flask的json数据"""
        if jsonData["M"] == "say":
            targetID = jsonData["TID"]
            find = session.query(DevicesTable).filter_by(ID=targetID).first()
            if find is None or find.status == 0:
                print("flaskJsonData:device off line")
                return
            deviceSockets[targetID].send(bytes(jsonData["C"]))
        elif jsonData["M"] == "checkout":
            targetID = jsonData["TID"]
            find = session.query(DevicesTable).filter_by(ID=targetID).first()
            if find is None or find.status == 0:
                print("flaskJsonData:Already OffLine")
                return
            targetData = """{"M":"checkout","IP":"{}","T":"{}"}\n""".format(str(clientAddress), time.time())
            deviceSockets.get(targetID).send(bytes(targetData))
            session.query(DevicesTable).filter_by(ID=targetData).update({"status": 0})
            session.commit()
            if lock.acquire():
                deviceSockets.pop(targetID)
                lock.release()
