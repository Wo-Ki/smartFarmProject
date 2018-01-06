# coding:utf-8
# /usr/bin/python

import requests
import socket

def handleFunc(clientSocket):
	while True:
		requestData = clientSocket.recv(1024)
		if requestData:
			print "requestData:",requestData
		responseStartLine="HTTP/1.1 200 OK\r\n"
    	responseHeaders="Server: My server\r\n"
    	responseBody = "hello"
    	response = responseStartLine + responseHeaders + "\r\n" + responseBody
    	clientSocket.send(bytes(response))
    	clientSocket.close

    	
if __name__ == "__main__":
	serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    serverSocket.bind(("192.168.100.5", 8989))
    serverSocket.listen(5)

    while True:
    	clientSocket, clientAddress = serverSocket.accept()
    	print "*" * 30
        print "[%s, %s] : connected" % clientAddress
        handleFunc(clientSocket)