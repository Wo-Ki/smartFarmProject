# coding:utf-8
# /usr/bin/python

# creator = wangkai
# creation time = 2017/12/28 21:07

import select
import socket
from updateCtrl import UpdateCtrl

if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server_socket.bind(("192.168.100.3", 8989))
    server_socket.listen(5)
    server_socket.setblocking(False)

    r_list = [server_socket]
    w_list = []
    # key:客户端句柄，value：接收和发送的消息队列；用于收和发之间共享数据
    msg_queues = {}

    sqlCtrl = UpdateCtrl("192.168.100.3", "smartFarmTest", "root", "123456")

    print "******Smart Farm Server Online*****"

    try:
        while True:
            read_able, write_able, e = select.select(r_list, w_list, [], 2)
    except KeyboardInterrupt:
        print "******Smart Farm Server Offline*****"
        server_socket.close()
        sqlCtrl.close()
