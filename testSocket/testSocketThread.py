# coding:utf-8
# /usr/bin/python

# creator = wangkai
# creation time = 2017/12/24 14:35

import socket
import time
import json
import threading
# from MysqlUpdateCtrl import MysqlUpdateCtrl
from datetime import datetime
from threading import Lock
# from JsonDataManger import JsonDataManager
from JsonDataORMThread import JsonDataORMCtrl
from exts import session
from models import DevicesTable


class HandleClient(threading.Thread):
    """处理客户端"""

    def __init__(self, clientSocket, clientAddress, lock):
        super(HandleClient, self).__init__()
        self.clientSocket = clientSocket
        self.clientAddress = clientAddress
        # self.sqlCtrl = MysqlUpdateCtrl("192.168.100.3", "smartFarmTest", "root", "123456")

    def run(self):
        """处理客户端请求数据"""
        global deviceSockets

        self.clientSocket.settimeout(10)
        while True:
            try:
                requestData = self.clientSocket.recv(1024)
                if requestData:
                    # print "request data:", requestData
                    if requestData[0] == "{":
                        # 对设备发来的数据进行解析
                        try:
                            jsonData = json.loads(requestData)
                            # print type(jsonData)
                            print "deviceSockets_1:", deviceSockets
                            if lock.acquire():
                                if deviceSockets.get(str(jsonData["ID"])) is None:
                                    deviceSockets[str(jsonData["ID"])] = self.clientSocket
                                    print "deviceSockets[str(jsonData[ID])]:", deviceSockets[str(jsonData["ID"])]
                                lock.release()
                            # JsonDataORMCtrl.devicesJsonData(jsonData, self.clientSocket, self.sqlCtrl, deviceSockets)
                            JsonDataORMCtrl.devicesJsonData(jsonData, self.clientSocket, deviceSockets, lock)
                            # sql = "insert into DHT11Data (device_id, hum_value, tem_value, create_time) values (%s,%s,%s,%s)"
                            # sqlCtrl.cud(sql, (jsonData["ID"], jsonData["Hum"], jsonData["Tem"], datetime.now()))
                            # clientSocket.send(bytes("OK\r\n"))

                        except:
                            print "json load error!!!"
                    else:
                        # 对flask发来的数据进行解析
                        try:
                            requestLines = requestData.splitlines()
                            postJsonDataSource = requestLines[-1]
                            url_data_list = postJsonDataSource.split("&")
                            postJsonData = {}
                            for data in url_data_list:
                                sub_data = data.split('=')
                                postJsonData[sub_data[0]] = sub_data[1]
                            print "postJsonData:", postJsonData
                            # if deviceSockets.get(postJsonData["deviceID"]):
                            #     deviceSockets.get(postJsonData["deviceID"]).send(bytes(postJsonData["ctrl"]))
                            #     print "send already!!!"
                            JsonDataORMCtrl.flaskJsonData(postJsonData, clientAddress, deviceSockets, lock)
                        except:
                            print "web data analysis error!!!"

            except Exception, e:
                print e
                print "[%s, %s] : disconnect" % clientAddress

                self.clientSocket.close()
                try:
                    clientSocketID = list(deviceSockets.keys())[list(deviceSockets.values()).index(self.clientSocket)]
                    # sql = "update devicesTable set status=0 where ID = %s"
                    # self.sqlCtrl.cud(sql, (clientSocketID,))
                    session.query(DevicesTable).filter_by(ID=clientSocketID).update({"status": 0})
                    session.commit()
                    if self.clientSocket in deviceSockets.values():
                        if lock.acquire():
                            deviceSockets.pop(clientSocketID)
                            lock.release()
                            # self.sqlCtrl.close()
                except:
                    pass
                print "deviceSockets_2:", deviceSockets

                print "#" * 30
                return


if __name__ == "__main__":
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    serverSocket.bind(("192.168.100.3", 8989))
    serverSocket.listen(30)

    # jsonDataManager = JsonDataManager()
    # 全局变量，储存当前连接的设备socket
    deviceSockets = {}
    lock = Lock()
    print "******Smart Farm Server Online*****"

    try:
        while True:
            clientSocket, clientAddress = serverSocket.accept()
            print "*" * 30
            # print "deviceSockets:", deviceSockets
            print "[%s, %s] : connected" % clientAddress
            handleClientProcess = HandleClient(clientSocket, clientAddress, lock)
            handleClientProcess.start()
            # clientSocket.close()

    except KeyboardInterrupt:
        print "******Smart Farm Server Offline*****"
        serverSocket.close()
        # sqlCtrl.close()
