# -*- coding:utf-8 -*-
import time
import re
import logger
import logging
import os
from IP_Filtering import ip_fiter
from weiba_api import WB
class flightmode():
    def __init__(self, deviceid, port):
        self.deviceid = deviceid
        self.port = port

    def flightmode(self,m,t,filtering_mode):
        self.mode = m
        os.system('adb -s '+ self.deviceid +' shell am force-stop com.tencent.mm')
        while True:
            try:
                WB(self.deviceid).airplaneModeTigger()
                # os.popen('adb -s '+ self.deviceid +' shell settings put global airplane_mode_on 1')
                # os.popen('adb -s '+ self.deviceid +' shell am broadcast -a android.intent.action.AIRPLANE_MODE --ez state true')
                # logging.info(self.deviceid+u'-开启飞行模式')
                # time.sleep(5)
                # os.popen('adb -s '+ self.deviceid +' shell settings put global airplane_mode_on 0')
                # os.popen('adb -s '+ self.deviceid +' shell am broadcast -a android.intent.action.AIRPLANE_MODE --ez state false')
                # logging.info(self.deviceid + u'-关闭飞行模式')
                time.sleep(int(t))
            except:pass
            try:
                try:
                    self.ip = re.findall('"cip": "([0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3})"', os.popen(
                        'adb -s ' + self.deviceid + ' shell curl "http://pv.sohu.com/cityjson"').read())[0]
                except:
                    logging.info(self.deviceid + u'网络异常,请查看手机是否可以正常联网')
                logging.info(self.deviceid + u'-' + self.ip)
                if self.mode == '1':
                    if ip_fiter(self.deviceid,self.ip,filtering_mode) == True:
                        return self.ip
                    else:
                        pass
                if self.mode == '2':
                    return self.ip
            except:
                logging.info(self.deviceid + u'-暂无可用网络,请稍后再试')







