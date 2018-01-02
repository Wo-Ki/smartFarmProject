# coding:utf-8
# /usr/bin/python

# creator = wangkai
# creation time = 2017/12/24 14:35

import socket
import time
import json
import threading
from updateCtrl import UpdateCtrl
from datetime import datetime
from threading import Lock


class HandleClient(threading.Thread):
    def __init__(self, client_socket, client_address):
        super(HandleClient, self).__init__()
        self.client_socket = client_socket
        self.client_address = client_address

    def run(self):
        """处理客户端请求数据"""
        self.client_socket.settimeout(10)
        while True:
            try:
                request_data = self.client_socket.recv(1024)
                if request_data:
                    print "request data:", request_data
                    # 对设备发来的数据进行解析
                    try:
                        json_data = json.loads(request_data)
                        # print type(json_data)
                        print "device_sockets_1:", device_sockets
                        sql = "insert into DHT11Data (device_id, hum_value, tem_value, create_time) values (%s,%s,%s,%s)"
                        sqlCtrl.cud(sql, (json_data["ID"], json_data["Hum"], json_data["Tem"], datetime.now()))
                        client_socket.send(bytes("OK\r\n"))
                        if lock.acquire():
                            if device_sockets.get(str(json_data["ID"])) is None:
                                device_sockets[str(json_data["ID"])] = client_socket
                                print "device_sockets[str(json_data[ID])]:", device_sockets[str(json_data["ID"])]
                            lock.release()
                    except:
                        print "json load error!!!"
                        # local_school.device_1001 = client_socket

                    # 对flask发来的数据进行解析
                    try:
                        request_lines = request_data.splitlines()
                        post_json_data_source = request_lines[-1]
                        # post_json_data_source = re.match(r"\w+ +(/[^ ]*)", str(request_last_line)).group(1)
                        # print "post_json_data_source:", post_json_data_source
                        url_data_list = post_json_data_source.split("&")
                        post_json_data = {}
                        for data in url_data_list:
                            sub_data = data.split('=')
                            post_json_data[sub_data[0]] = sub_data[1]
                        print "post_json_data:", post_json_data
                        if device_sockets.get(post_json_data["device_id"]):
                            device_sockets.get(post_json_data["device_id"]).send(bytes(post_json_data["ctrl"]))
                            print "send already!!!"
                    except:
                        print "web data analysis error!!!"

            except Exception, e:
                print e
                print "[%s, %s] : disconnect" % client_address
                client_socket.close()

                if client_socket in device_sockets.values():
                    if lock.acquire():
                        device_sockets.pop(str(json_data["ID"]))
                        lock.release()
                print "device_sockets_2:", device_sockets

                print "#" * 30
                return


if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server_socket.bind(("192.168.100.3", 8989))
    server_socket.listen(5)

    sqlCtrl = UpdateCtrl("192.168.100.3", "smartFarmTest", "root", "123456")
    # local_school = threading.local()
    # 全局变量，储存当前连接的设备socket
    device_sockets = {}
    lock = Lock()
    print "******Smart Farm Server Online*****"

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print "*" * 30
            # print "device_sockets:", device_sockets
            print "[%s, %s] : connected" % client_address
            handle_client_process = HandleClient(client_socket, client_address)
            handle_client_process.start()
            # client_socket.close()

    except KeyboardInterrupt:
        print "******Smart Farm Server Offline*****"
        server_socket.close()
        sqlCtrl.close()
