# coding:utf-8
# /usr/bin/python

# creator = wangkai
# creation time = 2018/1/20 14:30

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine


HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'smartFarmTest'
USERNAME = 'root'
PASSWORD = '123456'
DB_URI = 'mysql+mysqldb://{}:{}@{}:{}/{}'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)

engine = create_engine(DB_URI, max_overflow=5)

Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()