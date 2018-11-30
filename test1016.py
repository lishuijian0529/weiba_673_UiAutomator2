# -*- coding:utf-8 -*-

import datetime
import re
import os
import requests
import json
import base64

import time
deviceid='db9c0d81'
folder = os.path.exists('./%s' % deviceid)
if not folder:
    os.makedirs('./%s' % deviceid)
else:
    pass
res = requests.get('http://193.112.218.104:89/api?str=Initialize').text
image = json.loads(res)['qrcode']
data_62 = json.loads(res)['data']
h = open("./%s/%s.jpg" % (deviceid, deviceid), "wb")
h.write(base64.b64decode(image))
h.close()
os.popen('adb -s %s push ./%s/%s.jpg  /sdcard/myData/%s.jpg' % (deviceid, deviceid,  deviceid,deviceid)).read()
time.sleep(2)
os.popen('adb -s %s shell mv /sdcard/myData/%s.jpg /sdcard/myData/scan.jpg' % (deviceid, deviceid)).read()
time.sleep(2)
os.popen('adb -s %s shell curl http://127.0.0.1:8089?api=scandCode' % deviceid)
time.sleep(3)
for i in range(0, 10):
    os.popen('adb -s %s shell input tap 524 1587' % deviceid)