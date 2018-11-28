# -*- coding:utf-8 -*-
import os
import requests
import re
import logging
import logger
import time

def newPhone(deviceid):
    while True:
        if os.popen('adb -s %s shell curl "http://127.0.0.1:8081?api=newPhone"'%deviceid).read() == 'true':
            res = os.popen('adb -s %s shell curl "http://127.0.0.1:8081?api=backups"'%deviceid).read()
            if res != None:
                return res

def Recover(deviceid,dd_cloud):
   if os.popen('adb -s %s shell curl "http://127.0.0.1:8081?api=recover\&info=%s"'%(deviceid,dd_cloud)).read() == 'true':
       return True

def getimgByuser():
    while True:
        url = "http://47.254.16.32/img/getimgByuser"
        data = {"username": (None,'zenglu520'), "password": (None, 'zenglu520')}
        res = requests.post(url, files=data).text
        if res != 'false':
            url = re.findall('(.*).png',res)[0]+'.png'
            ipad_data = re.findall('\|(.*?)7F',res)[0]+'7F'
            return url,ipad_data
        else:
            logging.info(u'-暂时无可提62,等待5秒继续取')
            time.sleep(5)


def yun_scan(deviceid,url):
        status = os.popen(
            'adb -s %s shell curl "http://127.0.0.1:8081?api=scandCode\&url=%s"' %(deviceid,url)).read()
        if status=='收到url,准备扫码!!':
            return True


if __name__ == '__main__':
    print getimgByuser()

