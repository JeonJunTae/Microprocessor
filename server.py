import cv2
import numpy as np
import time
from bottle import route, run, response, request, post
import requests


upperbody_detector = cv2.CascadeClassifier("./haarcascade_mcs_upperbody.xml")
check = 0
# xml 파일 : https://github.com/opencv/opencv_attic/tree/master/opencv/data/haarcascades

class VideoCamera(object): 
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self): 
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        bodys = upperbody_detector.detectMultiScale(gray, 1.3, 5)
        if len(bodys)>1:
            check = 1
        else:
            check = 0
        for (x, y, w, h) in bodys:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        # 상반신 탐지 : https://minimin2.tistory.com/139

        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
    
@route('/')
@route('login')
def login():
  return '''
      <form action='/login' method='post'>
          StudentID: <input name='studentid' type='text' />
          Password: <input name='password' type='password' />
          <input value='Login' type='submit' />
      </form>
         '''
def check_login(studentid, password):
  if studentid == '2018732041' and password == 'jjt':
    return True
  else:
    return False
    
def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
@route('/video_feed') 
def video_feed():
    response.content_type = 'multipart/x-mixed-replace; boundary=frame'
    return gen(VideoCamera())

# https://github.com/chorok-daddy/courses/blob/main/MP_Appl/Week12-2-2_rpi_web_stream.py

@post('/login') 
def login_auth():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if check_login(username, password):
        return '''
            <html>
            <head>
                <title>KW Linrary seat : NO.1</title>
            </head>
            <body>
                <h1>KW Linrary seat : NO.1</h1>
                <img id="bg" class="img-thumbnail" src="/video_feed"> 
            </body>
            </html>
            '''
    else:
        return '<p>Login failed!</p>'

run(host='172.20.10.10', port=8000, reloader=True)
#https://github.com/chorok-daddy/courses/blob/main/MP_Appl/Week12-2-2_rpi_web_stream.py
