# coding:utf-8
# /usr/bin/python

# creator = wangkai
# creation time = 2017/12/29 16:36

import socket
import time, json
from multiprocessing import Process, Manager, Lock
from datetime import datetime
from JsonDataORMProcess import JsonDataORMCtrl
import select
from models import DevicesTable
from exts import session


# class ClockProcess(multiprocessing.Process):
#     def __init__(self, interval):
#         multiprocessing.Process.__init__(self)
#         self.interval = interval
#
#     def run(self):
#         pass
def handle_client(clientSocket, clientAddress, devicesMsgDicts, lock):
    """处理客户端请求数据"""
    clientSocket.settimeout(10)
    ID = ""
    while 1:
        rlist = [clientSocket, ]
        readLists, writeLists, errorLists = select.select(rlist, [], [])
        for value in readLists:
            if value == clientSocket:
                value.settimeout(10)
                try:
                    requestData = value.recv(4096)
                except Exception:
                    print "[%s, %s] : disconnect" % clientAddress
                    print "#" * 30
                    clientSocket.close()
                    if session.query(DevicesTable).filter_by(ID=ID).first() is not None:
                        session.query(DevicesTable).filter_by(ID=ID).update({"status": 0})
                        session.commit()
                    return

                if requestData:
                    lock.acquire()
                    print "%:Recv Data:%", clientAddress, requestData
                    lock.release()

                    if requestData[0] == "{":
                        """设备"""
                        try:
                            jsonData = json.loads(requestData)
                            ID = jsonData.get("ID")
                            if jsonData.get("M") == "say" or jsonData.get("M") == 'checkout':
                                devicesMsgDicts[jsonData["TID"]] = {"M": jsonData["M"], "SID": jsonData.get("SID"),
                                                                    "C": jsonData.get('C')}
                            else:
                                JsonDataORMCtrl.devicesJsonData(jsonData, clientSocket, lock)
                        except:
                            print "json load error"
                    else:
                        try:
                            requestLines = requestData.splitlines()
                            postJsonDataSource = requestLines[-1]
                            url_data_list = postJsonDataSource.split("&")
                            postJsonData = {}
                            for data in url_data_list:
                                sub_data = data.split('=')
                                postJsonData[sub_data[0]] = sub_data[1]
                            print "postJsonData:", postJsonData
                        except:
                            print "web load error"
            elif value == devicesMsgDicts:
                if devicesMsgDicts.get(ID) is not None:
                    sayData = {"M": devicesMsgDicts[ID]["M"], "SID": devicesMsgDicts[ID]["SID"],
                               "TID": ID, "C": devicesMsgDicts[ID]["C"]}
                    JsonDataORMCtrl.devicesJsonData(sayData, clientSocket, lock)
                    devicesMsgDicts.pop(ID)


if __name__ == "__main__":
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    serverSocket.bind(("192.168.100.3", 8989))
    serverSocket.listen(5)
    manager = Manager()
    devicesMsgDicts = manager.dict()
    lock = Lock()

    print "******Smart Farm Server Online*****"

    try:
        while True:
            clientSocket, clientAddress = serverSocket.accept()
            print "*" * 30
            # print "clientSocket type:", clientSocket
            print "[%s, %s] : connected" % clientAddress
            handleClientProcess = Process(target=handle_client,
                                          args=(clientSocket, clientAddress, devicesMsgDicts, lock))
            handleClientProcess.daemon = True
            handleClientProcess.start()
            clientSocket.close()

    except KeyboardInterrupt:
        print "******Smart Farm Server Offline*****"
        serverSocket.close()
