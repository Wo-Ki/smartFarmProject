# coding:utf-8
import cv2
from base_camera import BaseCamera
import datetime
import time
import imutils
from models import GreenHouseImages
from MysqlUpdateCtrl import MysqlUpdateCtrl


class Camera(BaseCamera):
    video_source = 0
    min_area = 5000
    firstFrame = None
    sqlCtrl = MysqlUpdateCtrl("192.168.100.3", "smartFarmTest", "root", "123456")

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source

    @staticmethod
    def frames():
        camera = cv2.VideoCapture(Camera.video_source)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        while True:
            # read current frame
            (grabbed, frame) = camera.read()
            text = "Unoccupied"
            # 如果不能抓到一帧，说明到了视频结尾
            # if not grabbed:
            #     break
            frame = imutils.resize(frame, width=500)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)
            # 如果第一帧是None，对其进行初始化
            if Camera.firstFrame is None:
                Camera.firstFrame = gray.copy().astype("float")
                continue

            cv2.accumulateWeighted(gray, Camera.firstFrame, 0.5)
            # 计算当前帧和第一帧的不同
            frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(Camera.firstFrame))
            thresh = cv2.threshold(frameDelta, 5, 255, cv2.THRESH_BINARY)[1]

            # 扩展阈值图像填充孔洞，然后找到阈值图像上的轮廓
            thresh = cv2.dilate(thresh, None, iterations=2)
            (_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # 遍历轮廓
            for c in cnts:
                # if the contour is too small ,ignore it
                if cv2.contourArea(c) < Camera.min_area:
                    continue
                # 计算轮廓的边界，在当前帧中画出该框
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                text = "Occupied"
                # 在当前帧上写文字和日期
            cv2.putText(frame, "Greenhouse Room status:{}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 0, 255), 2)
            cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                        (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
            # 保存图片
            if text == "Occupied" :
                sql = "insert into greenHouseImages (imgData,create_time) values (%s, %s)"
                Camera.sqlCtrl.cud(sql, (cv2.imencode('.jpg', frame)[1].tobytes(), datetime.datetime.now()))

                # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', frame)[1].tobytes()

