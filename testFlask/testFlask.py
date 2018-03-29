# coding:utf-8
# /usr/bin/python

# creator = wangkai
# creation time = 2017/12/25 08:10 

from flask import Flask, render_template, Response, request, redirect, url_for, flash
from flask_bootstrap import Bootstrap
import config
from models import DevicesTable, DataChenTable, NotificationTable, AlertTable, LogTable, StatusTable, GreenHouseImages, \
    User
from flask_login import login_user, logout_user, current_user, login_required, LoginManager
from exts import db, login_manager
from sqlalchemy import or_
from camera_opencv import Camera
import json
import base64
import datetime
from forms import loginAndRegist

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
bootstrap = Bootstrap(app)
login_manager.init_app(app)


@app.route('/index')
@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login', methods=["POST", "GET"])
def login():
    form = loginAndRegist.LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        passwrod = form.password.data
        user = User.query.filter(User.email == email).first()
        if user is None:
            flash(message=u"用户不存在", category='error')
            return redirect(url_for("login"))
        elif not user.check_password(passwrod):
            flash(message=u"密码错误", category='error')
            return redirect(url_for("login"))
        else:
            login_user(user)
            return redirect(url_for('index'))
    return render_template("login.html", form=form, title=u'登录')


@app.route('/register', methods=["GET", "POST"])
def register():
    form = loginAndRegist.RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, name=form.username.data, password=form.password.data)
        find = User.query.filter(User.email == form.email.data).first()
        if find:
            flash(u"邮箱已经被注册", category='error')
            return redirect(url_for("register"))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template('register.html', form=form, title=u"注册")


# @login_manager.user_loader
# def load_user(id):
#     return User.query.get(id)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route('/aboutUs')
def aboutUs():
    return render_template('aboutUs.html')


@app.route("/greenhouse")
@login_required
def greenhouse():
    return render_template("greenhouse.html")


@app.route("/data/greenhouse/<value>", methods=["POST"])
def greenhouseData(value):
    if value == "In":
        data = db.session.query(DataChenTable.humIn, DataChenTable.temIn,
                                DataChenTable.create_time).order_by("-create_time").first()
        contexts = {"contexts": [data[0], data[1], str(data[2])]}
    elif value == "Out":
        data = db.session.query(DataChenTable.humOut, DataChenTable.temOut,
                                DataChenTable.create_time).order_by("-create_time").first()
        contexts = {"contexts": [data[0], data[1], str(data[2])]}
    elif value == "Soil1":
        data = db.session.query(DataChenTable.humSoil1, DataChenTable.temSoil1,
                                DataChenTable.create_time).order_by("-create_time").first()
        contexts = {"contexts": [data[0], data[1], str(data[2])]}
    elif value == "Soil2":
        data = db.session.query(DataChenTable.humSoil2, DataChenTable.temSoil2,
                                DataChenTable.create_time).order_by("-create_time").first()
        contexts = {"contexts": [data[0], data[1], str(data[2])]}
    elif value == "status":
        data1 = DevicesTable.query.filter(DevicesTable.ID == "1001").first().status
        data2 = StatusTable.query.filter(StatusTable.ID == "1001").first()
        titles = [i for i in StatusTable.__dict__.keys() if not i.find("col")]
        data2Dict = {}
        for title in titles:
            if getattr(data2, title):
                data2Dict[title] = ":".join(getattr(data2, title).split("_"))
        # print "data2Dict", data2Dict
        data2Json = json.dumps(data2Dict)
        contexts = {"contexts": [data1, data2Json]}
    elif value == "all":
        data = DataChenTable.query.order_by("-create_time").first()
        contexts = {"contexts": {"ID": data.ID, "temIn": data.temIn, "humIn": data.humIn, "temOut": data.temOut,
                                 "humOut": data.humOut, "temSoil1": data.temSoil1, "humSoil1": data.humSoil1,
                                 "temSoil2": data.temSoil2, "humSoil2": data.humSoil2,
                                 "create_time": str(data.create_time)}}

    json_data = json.dumps(contexts)
    # print "/data/greenhouse/ json_data:", json_data
    return json_data


lastLogNum = 0


@app.route("/data/greenhouse/log/<value>", methods=["POST"])
def greenhouseLog(value):
    global lastLogNum
    backData = {"contexts": []}

    if value == "all":
        datas = db.session.query(NotificationTable.num, NotificationTable.SID, NotificationTable.TID,
                                 NotificationTable.message,
                                 NotificationTable.create_time).all()
        for data in datas:
            backData["contexts"].append(
                {"num": data[0], "SID": data[1], "TID": data[2], "msg": data[3], "time": str(data[4])})
            lastLogNum = data[0]
    elif value == "one":
        data = db.session.query(NotificationTable.num, NotificationTable.SID, NotificationTable.TID,
                                NotificationTable.message,
                                NotificationTable.create_time).order_by("-create_time").first()
        if lastLogNum != data[0]:
            lastLogNum = data[0]
            backData["contexts"].append(
                {"num": data[0], "SID": data[1], "TID": data[2], "msg": data[3], "time": str(data[4])})
        else:
            return json.dumps({"contexts": "None"})
    else:
        print "error greenhouseLog"

    print "log data:", json.dumps(backData)
    return json.dumps(backData)


@app.route("/greenhouseHis/<page>")
@login_required
def greenhouseHis(page):
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


@app.route("/data/greenhouseHis/<page>", methods=["POST"])
def greenhouseHisData(page):
    if page == "In":
        oldData = db.session.query(DataChenTable.humIn, DataChenTable.temIn, DataChenTable.create_time).all()
        contexts = {"contexts": [[i[0], i[1], str(i[2])] for i in oldData]}
        print "oldData:", contexts["contexts"][0]
        jsonData = json.dumps(contexts)
        print "jsonData type:", type(jsonData)
        return jsonData


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route("/monitorDataGreenhouse/")
def monitorDataGreenhouse():
    return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/monitor/", methods=["GET", "POST"])
@login_required
def monitor():
    if request.method == "GET":
        return render_template("monitor.html")
    else:

        imgsData = GreenHouseImages.query.order_by("-create_time").all()
        datePick = request.form.get("datePick")
        returnData = []
        if datePick == "option01":
            for value in imgsData:
                if datetime.datetime.now().day - value.create_time.day > 1:
                    break
                returnData.append(value)
        elif datePick == "option02":
            for value in imgsData:
                if datetime.datetime.now().day - value.create_time.day > 7:
                    break
                returnData.append(value)
        elif datePick == "option03":
            for value in imgsData:
                if datetime.datetime.now().day - value.create_time.day > 30:
                    break
                returnData.append(value)
        elif datePick == "option04":
            returnData = imgsData
        return render_template("monitor.html", imgsData=returnData, base64=base64)
        # return redirect(url_for("monitor", imgsData=returnData, base64=base64, _anchor="his"))


@app.route("/monitorHis/", methods=["GET", "POST"])
@login_required
def monitorHis():
    if request.method == "GET":
        return render_template("monitorHis.html")
    elif request.method == "POST":
        imgsData = GreenHouseImages.query.order_by("-create_time").all()
        datePick = request.form.get("datePick")
        returnData = []
        if datePick == "option01":
            for value in imgsData:
                if datetime.datetime.now().day - value.create_time.day > 1:
                    break
                returnData.append(value)
        elif datePick == "option02":
            for value in imgsData:
                if datetime.datetime.now().day - value.create_time.day > 7:
                    break
                returnData.append(value)
        elif datePick == "option03":
            for value in imgsData:
                if datetime.datetime.now().day - value.create_time.day > 30:
                    break
                returnData.append(value)
        elif datePick == "option04":
            returnData = imgsData
        return render_template("monitorHis.html", imgsData=returnData, base64=base64)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html")


# @app.context_processor
# def my_context_processor():
#     print current_user
#     return {"user": current_user}


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True, threaded=True)
