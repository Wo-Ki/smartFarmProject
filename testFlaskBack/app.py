# coding:utf-8
# /usr/bin/python

# creator = wang kai
# creation time = 2017/12/25 19:07 


from flask import Flask
import config
from models import DHT11Data
from exts import db
from sqlalchemy import or_

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route('/')
def index():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)
