# coding:utf-8
# /usr/bin/python

# creator = wangkai
# creation time = 2017/12/25 19:08

# coding:utf8
import os

# DEBUG = True
SECRET_KEY = os.urandom(24)

HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'smartFarmTest'
USERNAME = 'root'
PASSWORD = '123456'
DB_URI = 'mysql+mysqldb://{}:{}@{}:{}/{}'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
WTF_CSRF_ENABLED = False

SSL_DISABLE = False
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_RECORD_QUERIES = True

BABEL_DEFAULT_LOCALE = 'zh'
