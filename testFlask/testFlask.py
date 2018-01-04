# coding:utf-8
# /usr/bin/python

# creator = wangkai
# creation time = 2017/12/25 08:10 


from flask import Flask, render_template
import config
from models import DevicesTable, DataChenTable, NotificationTable, AlertTable, LogTable, StatusTable
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


@app.route("/data/greenhouse/")
def data():
    newData = DataChenTable.query.order_by("-create_time").first()
    # json_data = {"id": newData.id, "device_id": device_id, "Hum": newData.hum_value, "Tem": newData.tem_value,
    #              "create_time": str(newData.create_time)}
    # json_data = json.dumps(newData)
    # json_data = json.loads(json_data)
    jsonData = {"ID": newData.ID, "temIn": newData.temIn, "humIn": newData.humIn, "temOut": newData.temOut,
                "humOut": newData.humOut, "temSoil1": newData.temSoil1, "humSoil1": newData.humSoil1,
                "temSoil2": newData.temSoil2, "humSoil2": newData.humSoil2, "create_time": str(newData.create_time)}
    json_data = json.dumps(jsonData)
    print "/data/greenhouse/ json_data:", json_data
    return json_data


@app.route("/data/greenhouse/<page>")
def greenhouse_his(page):
    if page == "In":
        return render_template("greenhouseHis/greenhouseIn.html")
    elif page == "Out":
        return render_template("greenhouseHis/greenhouseOut.html")
    elif page == "Soil1":
        return render_template("greenhouseHis/greenhouseSoil1.html")
    elif page == "Soil2":
        return render_template("greenhouseHis/greenhouseSoil2.html")
    else:
        return "Not Found"


if __name__ == '__main__':
    app.run(host="192.168.100.3", port=5001, debug=True)
