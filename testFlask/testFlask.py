# coding:utf-8
# /usr/bin/python

# creator = wangkai
# creation time = 2017/12/25 08:10 


from flask import Flask, render_template
import config
from models import DevicesTable, DataChenTable, NotificationTable, AlertTable, LogTable
from exts import db
from sqlalchemy import or_
import json

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route('/')
def index():
    return render_template("index.html")


@app.route("/greenhouse/")
def greenhouse():
    return render_template("greenhouse.html")


@app.route("/data/<device_id>/")
def data(device_id):
    dht11_data = DHT11Data.query.filter(device_id == DHT11Data.device_id).order_by("-create_time").first()
    json_data = {"id": dht11_data.id, "device_id": device_id, "Hum": dht11_data.hum_value, "Tem": dht11_data.tem_value,
                 "create_time": str(dht11_data.create_time)}
    json_data = json.dumps(json_data)
    # json_data = json.loads(json_data)
    print json_data
    return json_data


@app.route("/data/greenhouse_his")
def greenhouse_his():
    pass


if __name__ == '__main__':
    app.run(host="192.168.100.3", port=5001, debug=True)
