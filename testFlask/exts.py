# coding:utf-8
# /usr/bin/python

# creator = wangkai
# creation time = 2017/12/25 19:16

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'