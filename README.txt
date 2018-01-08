使用配置：

testSocket文件夹：
	修改testSocketThread.py
		24行：self.sqlCtrl = MysqlUpdateCtrl("192.168.100.3", "smartFarmTest", "root", "123456")
		97行：serverSocket.bind(("192.168.100.3", 8989))

testFlask文件夹：
  	修改testFlask.py
		99行：app.run(host="192.168.100.3", port=5001, debug=True, threaded=True)
	修改config.py:
	修改greenhouse.js:
	修改greenhouseHis.js:
