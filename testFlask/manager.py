# coding:utf-8
# /usr/bin/python

# creator = wangkai
# creation time = 2017/12/25 19:16

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from testFlask import app
from exts import db
from models import DevicesTable, DataChenTable, NotificationTable, AlertTable, LogTable, StatusTable

manager = Manager(app)

# 绑定app和db
migrate = Migrate(app, db)

# 添加迁移脚本的命令到manager中
manager.add_command("db", MigrateCommand)

if __name__ == "__main__":
    manager.run()
