# coding:utf-8
# /usr/bin/python

# creator = wangkai
# creation time = 2017/12/25 19:17

from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class DHT11Data(db.Model):
    __tablename__ = "DHT11Data"
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    device_id = db.Column(db.Integer, nullable=False)
    hum_value = db.Column(db.Float, default="1.1")
    tem_value = db.Column(db.Float, default="1.1")
    create_time = db.Column(db.DateTime, default=datetime.now)
