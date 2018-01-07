# coding:utf-8
# /usr/bin/python

# creator = wangkai
# creation time = 2017/12/25 19:17

from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


# class DHT11Data(db.Model):
#     __tablename__ = "DHT11Data"
#     id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
#     device_id = db.Column(db.Integer, nullable=False, default=0)
#     hum_value = db.Column(db.Float, default="1.1")
#     tem_value = db.Column(db.Float, default="1.1")
#     create_time = db.Column(db.DateTime, default=datetime.now)


class DevicesTable(db.Model):
    __tablename__ = "devicesTable"
    ID = db.Column(db.String(10), nullable=False, primary_key=True)
    status = db.Column(db.String(10), nullable=False, default=0)  # 0:下线，1：上线，2：警告
    changeTime = db.Column(db.DateTime, default=datetime.now)


class DataChenTable(db.Model):
    __tablename__ = "data1001Table"
    num = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ID = db.Column(db.String(10), db.ForeignKey('devicesTable.ID'))
    temIn = db.Column(db.String(10))
    humIn = db.Column(db.String(10))
    temOut = db.Column(db.String(10))
    humOut = db.Column(db.String(10))
    temSoil1 = db.Column(db.String(10))
    humSoil1 = db.Column(db.String(10))
    temSoil2 = db.Column(db.String(10))
    humSoil2 = db.Column(db.String(10))
    # windCtrl = db.Column(db.String(10))
    # temCtrl = db.Column(db.String(10))
    # water1 = db.Column(db.String(10))  # 1:浇水， 0：不浇水
    # water2 = db.Column(db.String(10))  # 1:浇水， 0：不浇水
    # humanStatus = db.Column(db.String(10))  # 1:刷卡有人，2：异常有人，0：无人
    create_time = db.Column(db.DateTime, default=datetime.now)


class NotificationTable(db.Model):
    __tablename__ = "notificationTable"
    num = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    SID = db.Column(db.String(10), db.ForeignKey("devicesTable.ID"))
    TID = db.Column(db.Text)  # 目标设备ID，可能多个，以都好分隔
    message = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.now)


class AlertTable(db.Model):
    __tablename__ = "alertTable"
    num = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    ID = db.Column(db.String(10), db.ForeignKey('devicesTable.ID'))
    # deviceID = db.Column(db.String(10), db.ForeignKey("devicesTable.deviceID"))
    # targetID = db.Column(db.Text)  # 目标设备ID，可能多个，以都好分隔
    message = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.now)


class LogTable(db.Model):
    __tablename__ = "logTable"
    num = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    create_time = db.Column(db.DateTime, default=datetime.now)
    log = db.Column(db.Text, nullable=False)


class StatusTable(db.Model):
    __tablename__ = "statusTable"
    num = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    ID = db.Column(db.String(10), db.ForeignKey("devicesTable.ID"))
    changeTime = db.Column(db.DateTime, default=datetime.now)
    col1 = db.Column(db.String(50))
    col2 = db.Column(db.String(50))
    col3 = db.Column(db.String(50))
    col4 = db.Column(db.String(50))
    col5 = db.Column(db.String(50))
    col6 = db.Column(db.String(50))
    col7 = db.Column(db.String(50))


class GreenHouseImages(db.Model):
    __tablename__ = "greenHouseImages"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    imgData = db.Column(db.BLOB)
    create_time = db.Column(db.DateTime, default=datetime.now)
