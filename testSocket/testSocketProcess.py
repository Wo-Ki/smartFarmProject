# coding:utf-8
# /usr/bin/python

# creator = wangkai
# creation time = 2017/12/29 16:36

import socket
import time, json
from multiprocessing import Process, Manager
from updateCtrl import UpdateCtrl
from datetime import datetime
import re
import cPickle as pickle

# class ClockProcess(multiprocessing.Process):
#     def __init__(self, interval):
#         multiprocessing.Process.__init__(self)
#         self.interval = interval
#
#     def run(self):
#         pass
def handle_client(client_socket, client_address):
    """处理客户端请求数据"""
    while 1:

        client_socket.settimeout(10)
        while True:
            try:
                request_data = client_socket.recv(1024)
                if request_data:
                    print "request data", request_data
                    # mysql
                    # json_data = json.dumps(request_data)
                    try:
                        json_data = json.loads(request_data)
                        # print type(json_data)
                        sql = "insert into DHT11Data (device_id, hum_value, tem_value, create_time) values (%s,%s,%s,%s)"
                        sqlCtrl.cud(sql, (json_data["ID"], json_data["Hum"], json_data["Tem"], datetime.now()))
                        if not client_sockets.get(str(json_data["ID"])):
                            # pick_socket = pickle.dumps(client_socket)
                            client_sockets[json_data["ID"]] = [client_socket]
                            # client_sockets[str(json_data["ID"])] = "new"
                            # client_sockets[json_data["ID"]] = "now "
                            print "test:", client_sockets
                        print "client_sockets_1:", client_sockets
                    except:
                        print "json loads error!"
                    try:
                        request_lines = request_data.splitlines()
                        post_json_data_source = request_lines[-1]
                        # post_json_data_source = re.match(r"\w+ +(/[^ ]*)", str(request_last_line)).group(1)
                        # print "post_json_data_source:", post_json_data_source
                        url_data_list = post_json_data_source.split("&")
                        post_json_data = {}
                        for data in url_data_list:
                            sub_data = data.split('=')
                        #     post_json_data[sub_data[0]] = sub_data[1]
                        # print "post_json_data:", post_json_data
                        # print "client_sockets_3:",client_sockets
                        # print "post_json_data[device_id]", post_json_data["device_id"]
                        # print "client_sockets.get(post_json_data[device_id]):", client_sockets[post_json_data["device_id"]]
                        if client_sockets.get(post_json_data["device_id"]):
                            # client_sockets.get(post_json_data["device_id"]).send(bytes(post_json_data["ctrl"]))
                            # print "client_socket device_id:" ,client_sockets.get(post_json_data["device_id"])
                            client_socket.sendto("haha\r\n", ("192.168.100.12", 999))

                    except:
                        print "web error"

                    client_socket.send(bytes("OK\r\n"))
            except Exception, e:
                # print e
                # print "[%s, %s] : disconnect" % client_address
                # print "#" * 30
                # client_socket.close()
                # return
                print e
                print "[%s, %s] : disconnect" % client_address
                client_socket.close()
                try:
                    if json_data:
                        client_sockets.pop(json_data["ID"])
                    print "client_sockets_2:", client_sockets
                except:
                    pass

                print "#" * 30
                return


if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server_socket.bind(("192.168.100.3", 8989))
    server_socket.listen(5)
    manager = Manager()
    client_sockets = manager.dict()
    sqlCtrl = UpdateCtrl("192.168.100.3", "smartFarmTest", "root", "123456")
    print "******Smart Farm Server Online*****"

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print "*" * 30
            # print "client_socket type:", client_socket
            print "[%s, %s] : connected" % client_address
            handle_client_process = Process(target=handle_client, args=(client_socket, client_address))
            handle_client_process.daemon = True
            handle_client_process.start()
            client_socket.close()

    except KeyboardInterrupt:
        print "******Smart Farm Server Offline*****"
        server_socket.close()
        sqlCtrl.close()
