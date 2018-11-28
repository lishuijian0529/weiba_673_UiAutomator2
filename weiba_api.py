# -*- coding: utf-8 -*-
import re
import os
import logging
import logger
import time
import json
import os
import base64
import requests
class WB():
    def __init__(self,device):
        self.device = device
        self.head = '-H "Content-Type:application/json"'
        self.url = 'http://127.0.0.1:8888/cmd'
        self.timeout = '--connect-timeout 100'

    #获取微霸账号ID
    def get_weiba_account(self):
        while True:
            if self.test() == True:
                return re.findall('"data":"(.*?)"',
                           os.popen('adb -s %s shell curl "http://127.0.0.1:8888/cmd?group=AppTool\&action=deviceId"'%self.device).read())[0]

    #测试接口测试能调通
    def test(self):
        try:
            status = os.popen('adb -s %s shell curl http://127.0.0.1:8888'%self.device).read()
            if status == 'OK':
               return True
            else:
                logging.info(self.device + u'-无法获取到微霸后台启动,请关闭微霸重新开启')
        except:
            logging.info(self.device + u'-微霸测试接口调用失败')

    #一键新机
    def newDevice(self):
        while True:
            if self.freshAuth() == True:
                if self.test() == True:
                    status = os.popen('adb -s %s shell curl %s %s %s -X POST -d {"group":"AppTool"\,"action":"newDevice"\,"params":["com.tencent.mm"]} '%(self.device,self.timeout,self.head,self.url)).read()
                    st = json.loads(status)['success']
                    if st == 1:
                       return True
                else:
                    logging.info(self.device + u'-后台微霸未启动')


    #获取当前微信账号数据
    def get_wxid(self):
        while True:
            try:
                if self.freshAuth()==True:
                    if self.test() == True:
                        time.sleep(2)
                        status = os.popen('adb -s %s shell curl %s %s %s -X POST -d {"group":"AppTool"\,"action":"getCurrentAppAccount"\,"params":["com.tencent.mm"]}'%(self.device,self.timeout,self.head,self.url)).read()
                        st = json.loads(status)['success']
                        if st == 1:
                            json_data= json.loads(status)
                            wxid=json_data['data']['strWxUUID']
                            return wxid
                        else:time.sleep(2)
                    else:
                        logging.info(self.device + u'-后台微霸未启动')
            except:
                logging.info(self.device+u'-获取微信ID失败,重新获取')
                time.sleep(2)
    #保存当前微信数据
    def save_wechat_data(self,ph,wxid,wxmc):
        while True:
            if self.freshAuth()==True:
                if self.test() == True:
                    status = os.popen(
                        'adb -s %s shell curl %s %s %s -X POST -d {"group":"AppTool"\,"action":"accountStore"\,"params":[{"strId":"%s"\,"strPkg":"com.tencent.mm"\,"strWxUUID":"%s"\,"strName":"%s"}]}'%(self.device,self.timeout,self.head,self.url,ph,wxid,wxmc)).read()
                    st = json.loads(status)['success']
                    if st == 1:
                        if len(json.loads(status)) == 1:
                            logging.info(self.device + u'-微霸数据保存成功')
                            return True
                        else:
                            logging.info(self.device + '-' + json.loads(status)['data'] )
                else:
                    logging.info(self.device + u'-后台微霸未启动')


    #切换微霸环境
    def switch_wechat_data(self, wxid):
        while True:
            if self.freshAuth()==True:
                try:
                    if self.test()== True:
                        status = os.popen(
                            'adb -s ' + self.device + ' shell curl '+self.timeout+' -g "http://127.0.0.1:8888/cmd?group=AppTool\&action=accountRecover\&params=[%22/sdcard/Download/weiba/wx/"' + wxid + '".wbwx%22]"').read()
                        st = json.loads(status)['success']
                        if st == 1:
                            if json.loads(status).__len__() == 1:
                                logging.info(self.device + u'-环境切换成功')
                                return True
                            else:
                                logging.info(self.device + u'-' + json.loads(status)['data'])
                                if '文件未指定'.decode('utf-8') in json.loads(status)['data']:
                                    logging.info(u'%s-该手机没有这个数据:%s' % (self.device, wxid))
                                    return False
                    else:
                        logging.info(self.device+u'-后台微霸未启动')
                except:
                    logging.info(self.device+u'-环境切换失败')
            else:
                logging.info(self.device + u'-微霸授权刷新失败,重新刷新授权')

    #生成云码
    def getCloudCode(self, ph):
        while True:
            if self.test() == True:
                status = os.popen(
                    'adb -s %s shell curl %s %s %s -X POST -d {"group":"AppTool"\,"action":"genCloudCode"\,"params":[{"strId":"%s"\,"strPkg":"com.tencent.mm"\,"strApp":"wx"\,"strName":"wx"}]}'%(self.device,self.timeout,self.head,self.url,ph)).read()
                st = json.loads(status)['success']
                if st == 1:
                    if len(json.loads(status)['data'])!=0:
                        logging.info(self.device+u'-云码提取成功:'+json.loads(status)['data'])
                        return json.loads(status)['data']
                    else:
                        logging.info(u'%s-获取云码失败,重新获取'%(self.device))
            else:
                logging.info(self.device + u'-后台微霸未启动')

    def cloudCodeRecover(self, cloudCode):
        if self.test() == True:
            status=os.popen("adb -s %s shell curl -g -H \\\"Content-Type:application/json\\\" \\\"http://127.0.0.1:8888/cmd\\\" -X POST -d '{\\\"group\\\":\\\"AppTool\\\",\\\"action\\\":\\\"cloudCodeRecover\\\",\\\"params\\\":[\\\"%s\\\"]}'" % (self.device,cloudCode)).read()
            if json.loads(status)['data'] == True:
                logging.info(self.device + u'-云码恢复成功')
                return True
            else:
                logging.info(self.device+u'-云码恢复失败')
        else:
            logging.info(self.device + u'-后台微霸未启动')

    def get_accounts(self):
        if self.freshAuth() == True:
            try:
                if self.test() == True:
                    if self.test() == True:
                        status = os.popen('adb -s '+self.device+' shell curl -g "http://127.0.0.1:8888/cmd?group=AppTool\&action=getAppAccounts\&params=[%22com.tencent.mm%22]"').read()
                        return status
            except:pass

    def freshAuth(self):
        try:
            #os.popen('adb -s ' + self.device + ' shell am start com.miui.miuibbs/.MainActivity')
            os.popen('adb -s ' + self.device + ' shell am start com.miui.miuibbs/com.miui.miuibbs.MainActivity')
            time.sleep(3)
            logging.info(self.device+u'-正在刷新微霸授权,请稍后')
            status=os.popen('adb -s %s shell curl %s %s %s -X POST -d {"group":"AppTool"\,"action":"freshAuth"} '%(self.device,self.timeout,self.head,self.url)).read()
            if  json.loads(status)['success'] == 1:
                return True
        except:
            logging.info(self.device + u'-检测微霸未开启,程序自动开启微霸')

    def scancode(self):
        status = os.popen(
            'adb -s ' + self.device + ' shell curl -g "http://127.0.0.1:8888/cmd?group=AppTool\&action=wxStartScan\&params=[%22\/sdcard\/myData\/scan.png%22]"').read()
        print status

    def airplaneModeTigger(self):
        while True:
            if self.freshAuth()==True:
                try:
                    if self.test()== True:
                        logging.info(u'%s-正在切换飞行'%self.device)
                        os.popen('adb -s %s shell curl "http://127.0.0.1:8888/cmd?group=AppTool\&action=airplaneModeTigger"'%self.device)
                        logging.info(u'%s-切换飞行成功'%self.device)
                        break
                    else:
                        logging.info(self.device+u'-后台微霸未启动')
                except:
                    logging.info(self.device+u'-环境切换失败')
            else:
                logging.info(self.device + u'-微霸授权刷新失败,重新刷新授权')



if __name__ == '__main__':

    a = WB('db9c0d81').airplaneModeTigger()

