# -*- coding:utf-8 -*-
import os
import time
from OpenPhone import Open
from File import file
import logger
import requests
import logging
import random
import datetime
from appium.webdriver.common.touch_action import TouchAction
import duoduo_api
import TokenYZ
from Token import token
from weiba_api import WB
import json
import base64
import re

class login_wechat():
    def __init__(self, deviceid, port, gj_mode, country=None, gj=None, wxid=None, login_mode=None, cloudCode=None, ip=None, date=None):
        self.deviceid = deviceid
        self.port = port
        self.om = file().readOperationMode()
        self.gj_mode = gj_mode
        self.wb_appPackage = 'com.md188.weiba'
        self.wb_appActivity = '.MainActivity'
        self.dd_appPackage = file().readuser()[25].strip('\n')
        self.dd_appActivity = file().readuser()[26].strip('\n')
        self.country = country
        self.gj = gj
        self.w = WB(self.deviceid)
        self.wxid = wxid
        self.login_mode = login_mode
        self.cloudCode = cloudCode
        self.ip = ip
        self.date = date
        self.element_json = json.loads(file.read_all('6.7.3.json'))
        self.w = WB(deviceid)

    def wb_login(self, ph, mm):
        if self.login_mode == '1.wxid登陆'.decode("utf-8"):
            if self.w.switch_wechat_data(self.wxid) == True:
                self.driver = Open().Phone('com.tencent.mm', '.ui.LauncherUI', self.deviceid, self.port)
                self.driver.implicitly_wait(60)
                return ph, mm
            else:
                raise quit()
        if self.login_mode == '2.云码登陆'.decode("utf-8"):
            if self.w.cloudCodeRecover(self.cloudCode) == True:
                self.driver = Open().Phone('com.tencent.mm', '.ui.LauncherUI', self.deviceid, self.port)
                self.driver.implicitly_wait(60)
                return ph, mm

    def visualization(self, message):
        try:
            requests.get('http://127.0.0.1:666/query?time=%s&number=%s&state=%s' % (int(time.time()), self.deviceid, message))
        except:pass

    def dd_switch(self, ph, mm, device_token):
        if duoduo_api.Recover(self.deviceid,device_token) == True:
            self.visualization('环境还原成功')
            logging.info(self.deviceid+u'-环境还原成功')
            self.driver = Open().Phone('com.tencent.mm', '.ui.LauncherUI', self.deviceid, self.port)
            self.driver.implicitly_wait(60)
        self.visualization('启动')
        logging.info(self.deviceid + u'-启动')
        return ph, mm

    def error_message(self):
        while True:
            if '外挂' in self.cw.encode('utf-8'):
                return 'waigua'
            if '批量' in self.cw.encode('utf-8'):
                return 'piliang'
            if '密码错误' in self.cw.encode('utf-8'):
                return 'piliang'
            if '多人投诉' in self.cw.encode('utf-8'):
                return 'tousu'
            if '系统检测' in self.cw.encode('utf-8'):
                return 'xitong'
            if '微信登陆环境存在异常' in self.cw.encode('utf-8'):
                return 'huanjingyichang'
            if '添加好友' in self.cw.encode('utf-8'):
                return 'tianjia'
            if '使用存在异常' in self.cw.encode('utf-8'):
                return 'shiyongyichang'
            if '传播色情' in self.cw.encode('utf-8'):
                return 'seqing'
            if '长期未登陆' in self.cw.encode('utf-8'):
                return 'changqi'
            if '你的微信号由于长期' in self.cw.encode('utf-8'):
                return 'weishiyong'
            if '解封环境异常' in self.cw.encode('utf-8'):
                return 'jiefengyichang'
            if '手机通讯录' in self.cw.encode('utf-8'):
                self.driver.find_element_by_name('否').click()
                return None
            if '表情' in self.cw.encode('utf-8'):
                self.driver.find_element_by_name('　取消　').click()
                return None
            if '通过短信验证码' in self.cw.encode('utf-8'):
                self.driver.find_element_by_name('确定').click()
                return None
            if '注册了新的微信号' in self.cw.encode('utf-8'):
                return 'newwechat'

    def mm_login(self, ph, mm):
        time.sleep(10)
        self.driver.implicitly_wait(2)
        while True:
            #如果出现输入框
            if self.driver.find_elements_by_id(self.element_json[u'输入框ID'])!=[]:
                self.driver.implicitly_wait(10)
                os.system('adb -s %s shell input text %s' % (self.deviceid, mm))
                self.visualization('输入密码')
                logging.info(self.deviceid + u'-输入密码')
                self.driver.find_element_by_id(self.element_json[u'输入密码登陆按钮ID']).click()
                self.visualization('点击登陆')
                logging.info(self.deviceid + u'-点击登录')
                if self.driver.find_elements_by_id(self.element_json[u'错误弹窗内容ID'])!=[]:
                    # 判断是否登录不上
                    self.cw = self.driver.find_element_by_id(self.element_json[u'错误弹窗内容ID']).get_attribute(('text'))
                    if '表情' in self.cw.encode('utf-8'):
                        self.driver.find_element_by_name('取消').click()
                        break
                    if '通过微信密码' in self.cw.encode('utf-8'):
                        self.driver.find_element_by_name('忽略').click()
                        break
                    else:
                        return self.error_message()
            #如果出现错误弹窗
            if self.driver.find_elements_by_id(self.element_json[u'错误弹窗内容ID'])!=[]:
                logging.info(u'%s-出现错误弹窗'%self.deviceid)
                self.cw = self.driver.find_element_by_id(self.element_json[u'错误弹窗内容ID']).get_attribute(('text'))
                if '表情' in self.cw.encode('utf-8'):
                    self.driver.find_element_by_name('　取消　').click()
                if '通过微信密码' in self.cw.encode('utf-8'):
                    self.driver.find_element_by_name('忽略').click()
                    break
                else:
                    self.driver.implicitly_wait(60)
                    self.driver.find_element_by_id(self.element_json[u'错误弹窗确定ID']).click()
                    self.visualization('登陆出现错误')
                    time.sleep(8)
                    os.popen('adb -s %s shell am start -n com.tencent.mm/.ui.LauncherUI' % self.deviceid).read()
                    self.driver.find_element_by_id(self.element_json[u'输入框ID']).send_keys(mm)
                    self.visualization('输入密码')
                    logging.info(self.deviceid + u'-输入密码')
                    self.driver.find_element_by_id(self.element_json[u'输入密码登陆按钮ID']).click()
                    self.visualization('点击登陆')
                    logging.info(self.deviceid + u'-点击登录')
                    time.sleep(12)
                    self.driver.implicitly_wait(2)
                    while True:
                        if self.driver.find_elements_by_id(self.element_json[u'错误弹窗内容ID'])!=[]:
                        #判断是否登录不上
                            self.cw = self.driver.find_element_by_id(self.element_json[u'错误弹窗内容ID']).get_attribute(('text'))
                            return self.error_message()
                        if self.driver.find_elements_by_id(self.element_json[u'微信四个主按钮ID']) != []:
                            break
            #如果进入微信页面
            if self.driver.find_elements_by_id(self.element_json[u'微信四个主按钮ID'])!=[]:
                break
            #如果进入微信首页
            if self.driver.find_elements_by_name('登录')!=[]:
                self.Home_Login(ph,mm)
                if self.driver.find_elements_by_id(self.element_json[u'错误弹窗内容ID'])!=[]:
                    self.cw = self.driver.find_element_by_id(self.element_json[u'错误弹窗内容ID']).get_attribute(('text'))
                    return self.error_message()
            if 'com.tencent.mm' not in os.popen('adb -s %s shell dumpsys activity | findstr "mFocusedActivity"'%self.deviceid).read():
                os.popen('adb -s %s shell am start -n com.tencent.mm/.ui.LauncherUI' % self.deviceid).read()

    def Home_Login(self,ph,mm):
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_name('登录').click()
        self.driver.find_element_by_id(self.element_json[u'输入框ID']).click()
        os.system('adb -s %s shell input text %s' % (self.deviceid, ph))
        logging.info(self.deviceid + u'-输入账号')
        self.visualization('输入账号')
        self.driver.find_element_by_id(self.element_json[u'输入手机号码登陆下一步']).click()
        self.visualization('下一步')
        logging.info(self.deviceid + u'-下一步')
        self.driver.find_elements_by_id(self.element_json[u'输入框ID'])[1].click()
        os.system('adb -s %s shell input text %s' % (self.deviceid, mm))
        self.visualization('输入密码')
        logging.info(self.deviceid + u'-输入密码')
        self.driver.find_element_by_id(self.element_json[u'输入手机号码登陆下一步']).click()
        self.visualization('登录')
        logging.info(self.deviceid + u'-登录')

    def zh_login(self, wechat_list):
        self.driver.implicitly_wait(5)
        if self.driver.find_elements_by_name(self.element_json['allow'])!=[]:
            self.driver.find_element_by_name(self.element_json['allow']).click()
            self.driver.find_element_by_name(self.element_json['allow']).click()
        self.driver.implicitly_wait(30)
        self.driver.find_element_by_name(self.element_json['login']).click()
        self.driver.find_element_by_id(self.element_json[u'输入框ID']).click()
        os.system('adb -s %s shell input text %s' % (self.deviceid, wechat_list[0]))
        self.visualization('输入账号')
        logging.info(self.deviceid + u'-输入账号')
        self.driver.find_element_by_id(self.element_json[u'输入手机号码登陆下一步']).click()
        self.visualization('下一步')
        logging.info(self.deviceid + u'-下一步')
        self.driver.find_elements_by_id(self.element_json[u'输入框ID'])[1].click()
        os.system('adb -s %s shell input text %s' % (self.deviceid, wechat_list[1]))
        self.visualization('输入密码')
        logging.info(self.deviceid + u'-输入密码')
        self.driver.find_element_by_id(self.element_json[u'输入手机号码登陆下一步']).click()
        self.visualization('登录')
        logging.info(self.deviceid + u'-登录')
        self.driver.implicitly_wait(2)
        while True:
            if self.driver.find_elements_by_id(self.element_json[u'错误弹窗内容ID'])!=[]:
                self.cw = self.driver.find_element_by_id(self.element_json[u'错误弹窗内容ID']).get_attribute(('text'))
                return self.error_message()
            if self.driver.find_elements_by_id(self.element_json[u'微信四个主按钮ID']) != []:
                break
            if self.driver.find_elements_by_android_uiautomator('new UiSelector().description("拖动下方滑块完成拼图")') != []:
                logging.info(u'%s-进入滑图页面'%self.deviceid)
                while True:
                    for j in range(100, 200, 30):
                        try:
                            a = TouchAction(self.driver)
                            a.press(x=250, y=1000)
                            for i in range(0, 5):
                                a.move_to(x=50, y=(random.randint(-500, 0))).wait(0)
                                a.move_to(x=50, y=(random.randint(0, 500))).wait(0)
                            for i in range(0, j / 10):
                                a.move_to(x=10, y=0).wait(100)
                            a.release().perform()
                        except:pass
                    if self.driver.find_elements_by_android_uiautomator('new UiSelector().description("开始验证 ")') != []:
                        file().write('%s\n' % wechat_list[0], '新设备记录文本.txt')
                        logging.info(u'%s-%s该账号出现新设备' % (self.deviceid, wechat_list[0]))
                        self.driver.quit()
                        break
                    if self.driver.find_elements_by_id(self.element_json[u'输入手机号码登陆下一步']) != []:
                        self.driver.find_element_by_id(self.element_json[u'输入手机号码登陆下一步']).click()
                        break
                    if self.driver.find_elements_by_android_uiautomator('new UiSelector().description("声音锁验证 ")') != []:
                        file().write('%s\n' % wechat_list[0], '新设备记录文本.txt')
                        logging.info(u'%s-%s该账号出现新设备' % (self.deviceid, wechat_list[0]))
                        self.driver.quit()
                        break
            if self.driver.find_elements_by_android_uiautomator('new UiSelector().description("开始验证 ")') != []:
                file().write('%s\n' % wechat_list[0], '新设备记录文本.txt')
                logging.info(u'%s-%s该账号出现新设备'%(self.deviceid,wechat_list[0]))
                self.driver.quit()
                break
    def upgrade(self):
        if self.driver.find_elements_by_name('微信团队邀请你参与内部体验')!=[]:
            self.driver.find_element_by_name('微信团队邀请你参与内部体验').click()

    def login_fail(self, error, wechat_list):
        if error == 'waigua':
            file().write('%s %s %s %s 外挂 %s\n' % (wechat_list[0], wechat_list[1], self.ip, self.date, self.deviceid),'登录异常账号.txt')
        if error == 'piliang':
            file().write('%s %s %s %s 批量 %s\n' %(wechat_list[0], wechat_list[1], self.ip, self.date, self.deviceid),'登录异常账号.txt')
        if error == 'mimacuowu':
            file().write('%s %s %s %s 密码错误 %s\n' % (wechat_list[0], wechat_list[1], self.ip, self.date, self.deviceid),'登录异常账号.txt')
        if error == 'tousu':
            file().write('%s %s %s %s 多人投诉被限制登陆 %s\n' % (wechat_list[0], wechat_list[1],self.ip,self.date, self.deviceid), '登录异常账号.txt')
        if error == 'jidiao':
            file().write('%s %s %s %s 在别的设备登陆过 %s\n' % (wechat_list[0], wechat_list[1],self.ip,self.date, self.deviceid),'登录异常账号.txt')
        if error == 'xitong':
            file().write('%s %s %s %s 系统检测到你的账号有异常 %s\n' % (wechat_list[0], wechat_list[1], self.ip,self.date,self.deviceid),'登录异常账号.txt')
        if error == 'huanjingyichang':
            file().write('%s %s %s %s 当前设备的微信登陆环境存在异常 %s\n' % (wechat_list[0], wechat_list[1],self.ip,self.date, self.deviceid),'登录异常账号.txt')
        if error == 'tianjia':
            file().write('%s %s %s %s 当前账号添加好友过于频繁 %s\n' % (wechat_list[0], wechat_list[1],self.ip,self.date ,self.deviceid),'登录异常账号.txt')
        if error == 'shiyongyichang':
            file().write('%s %s %s %s 当前账号的使用存在异常 %s\n' % (wechat_list[0], wechat_list[1], self.ip,self.date,self.deviceid),'登录异常账号.txt')
        if error == 'seqing':
            file().write('%s %s %s %s该微信账号因涉嫌传播色情 %s\n' % (wechat_list[0], wechat_list[1],self.ip,self.date, self.deviceid), '登录异常账号.txt')
        if error == 'changqi':
            file().write('%s %s %s %s 该账号长期未登陆 %s\n' % (wechat_list[0], wechat_list[1], self.ip,self.date,self.deviceid),'登录异常账号.txt')
        if error == 'huatu':
            file().write('%s %s %s %s 进入滑图页面 %s\n' % (wechat_list[0], wechat_list[1],self.ip,self.date, self.deviceid),'登录异常账号.txt')
        if error == 'weishiyong':
            file().write('%s %s %s %s 该账号长期未使用,已被收回 %s\n' % (wechat_list[0], wechat_list[1], self.ip, self.date, self.deviceid),'登录异常账号.txt')
        if error == 'jiefengyichang':
            file().write( '%s %s %s %s 解封环境异常 %s\n' % (wechat_list[0], wechat_list[1], self.ip, self.date, self.deviceid), '登录异常账号.txt')
        if error == 'newwechat':
            file().write('%s %s %s %s 注册了新的微信号 %s\n' % (wechat_list[0], wechat_list[1], self.ip, self.date, self.deviceid),'登录异常账号.txt')

    def add_friend(self, zh, mm, hy):
        time.sleep(10)
        self.driver.implicitly_wait(2)
        while True:
            if self.driver.find_elements_by_id(self.element_json[u'微信四个主按钮ID']) != []:
                break
            if self.driver.find_elements_by_id(self.element_json[u'错误弹窗内容ID']) != []:
                self.cw = self.driver.find_element_by_id(self.element_json[u'错误弹窗内容ID']).get_attribute(('text'))
                if '微信密码' in self.cw.encode('utf-8'):
                    self.driver.find_element_by_name('忽略').click()
                if '表情' in self.cw.encode('utf-8'):
                    self.driver.find_element_by_name('　取消　').click()
        self.driver.implicitly_wait(60)
        self.driver.find_element_by_id(self.element_json[u'微信页面加号']).click()
        self.driver.find_elements_by_id(self.element_json[u'加号列表'])[1].click()
        self.visualization('添加朋友')
        logging.info(self.deviceid + u'-添加朋友')
        self.driver.find_element_by_id(self.element_json[u'输入框ID']).click()
        time.sleep(2)
        self.driver.find_element_by_id(self.element_json[u'输入框ID']).send_keys(hy)
        self.driver.implicitly_wait(2)
        while True:
            if self.driver.find_elements_by_id(self.element_json[u'点击添加按钮']) != []:
                time.sleep(3)
                os.popen('adb -s %s shell input tap 600 300' % self.deviceid)
                #self.driver.find_element_by_id(self.element_json[u'点击添加按钮']).click()
            if self.driver.find_elements_by_id(self.element_json[u'设置备注'])!=[]:
                break
            if self.driver.find_elements_by_id(self.element_json[u'错误弹窗确定ID'])!=[]:
                self.driver.find_element_by_id(self.element_json[u'错误弹窗确定ID']).click()
                time.sleep(3)
                self.driver.find_element_by_id(self.element_json[u'点击添加按钮']).click()
            if self.driver.find_elements_by_name('该用户不存在')!=[]:
                self.driver.find_element_by_id(self.element_json[u'输入框ID']).clear()
                time.sleep(2)
                self.driver.find_element_by_id(self.element_json[u'输入框ID']).send_keys(hy)
        while True:
            if self.driver.find_elements_by_id(self.element_json[u'添加通讯录']) != []:
                self.driver.find_element_by_id(self.element_json[u'添加通讯录']).click()
            if self.driver.find_elements_by_id(self.element_json[u'发消息'])!=[]:
                self.driver.find_element_by_id(self.element_json[u'发消息']).click()
            if self.driver.find_elements_by_id(self.element_json[u'消息内容框ID'])!=[]:
                break
        self.driver.implicitly_wait(180)
        self.driver.find_element_by_id(self.element_json[u'消息内容框ID']).send_keys(zh)
        logging.info(self.deviceid + u'-正在发送信息:' + zh)
        self.visualization('正在发送信息:%s' % zh)
        time.sleep(3)
        while True:
            if self.driver.find_element_by_id(self.element_json[u'消息发送按钮ID'])!=[]:
                os.popen('adb -s %s shell input tap 1000 1839' % self.deviceid)
            if self.driver.find_elements_by_id('com.tencent.mm:id/mq')!=[]:
                break
        self.visualization('点击发送')
        logging.info(self.deviceid + u'-点击发送')
        time.sleep(2)
        file().write('%s_%s  %s  %s  %s  %s| %s\n' % (zh, mm, datetime.datetime.now().strftime('%Y-%m-%d'), self.deviceid, self.wxid, self.cloudCode, hy),'加好友成功列表.txt')
        while True:
            if self.w.save_wechat_data(zh, self.wxid,zh) == True:
                time.sleep(15)
                break


    def circle_of_friends(self):
        time.sleep(10)
        self.driver.implicitly_wait(2)
        while True:
            if self.driver.find_elements_by_id(self.element_json[u'微信四个主按钮ID'])!=[]:
                self.driver.find_elements_by_id(self.element_json[u'微信四个主按钮ID'])[2].click()
                break
            if self.driver.find_elements_by_id(self.element_json[u'错误弹窗内容ID'])!=[]:
                self.cw = self.driver.find_element_by_id(self.element_json[u'错误弹窗内容ID']).get_attribute(('text'))
                if '微信密码' in self.cw.encode('utf-8'):
                    self.driver.find_element_by_name('忽略').click()
                if '表情' in self.cw.encode('utf-8'):
                    self.driver.find_element_by_name('　取消　').click()
        self.driver.implicitly_wait(60)
        logging.info(self.deviceid + u'-点击发现')
        time.sleep(random.randint(1, 3))
        self.driver.find_elements_by_id(self.element_json[u'发现页面朋友圈ID'])[0].click()
        self.visualization('点击朋友圈')
        logging.info(self.deviceid + u'-点击朋友圈')
        time.sleep(5)
        if self.driver.find_elements_by_id(self.element_json[u'朋友圈相机ID'])!=[]:
            TouchAction(self.driver).long_press(self.driver.find_element_by_id(self.element_json[u'朋友圈相机ID']), 2000).release().perform()
            logging.info(self.deviceid + u'-长按相机')
            self.visualization('长按相机')
        self.driver.implicitly_wait(5)
        if self.driver.find_elements_by_id(self.element_json[u'发表按钮ID']) != []:
            self.input_message()
        else:
            time.sleep(random.randint(1, 2))
            self.driver.find_element_by_id(self.element_json[u'我知道了ID']).click()
            self.input_message()
        self.visualization('点击发表')
        logging.info(self.deviceid + u'-点击发表')
        self.driver.find_element_by_android_uiautomator(
            'new UiSelector().description("返回")').click()
        time.sleep(random.randint(1, 3))
        self.driver.find_element_by_id(self.element_json[u'微信四个主按钮ID']).click()
        time.sleep(random.randint(1, 3))
        file().write_pyq_succ('%s_%s  %s  %s  %s  %s|' % (
        self.wechat_list[0], self.wechat_list[1], datetime.datetime.now().strftime('%Y-%m-%d'), self.deviceid, self.
            wxid, self.cloudCode))
        while True:
            if self.w.save_wechat_data(self.wechat_list[0], self.wxid,self.wechat_list[0]) == True:
                time.sleep(15)
                break

    def input_message(self):
        time.sleep(random.randint(1, 2))
        self.visualization('进入到发文字朋友圈页面')
        logging.info(self.deviceid + u'-进入到发文字朋友圈页面')
        self.driver.find_element_by_id(self.element_json[u'朋友圈内容输入框ID']).click()
        self.driver.find_element_by_id(self.element_json[u'朋友圈内容输入框ID']).send_keys(file().sh())
        self.visualization('输入文字')
        logging.info(self.deviceid + u'-输入文字')
        time.sleep(random.randint(1, 2))
        self.driver.find_element_by_id(self.element_json[u'发表按钮ID']).click()
    #打开影子科技
    def start_yz(self):
        os.system('adb -s ' + self.deviceid + ' shell am force-stop wechatscancoder.jionego.com.wechatscancoder')
        os.popen('adb -s %s shell am start -n wechatscancoder.jionego.com.wechatscancoder/.MainActivity' % self.deviceid).read()
        time.sleep(3)
        os.popen('adb -s %s shell am start -n com.tencent.mm/.ui.LauncherUI' % self.deviceid).read()

    #获取62二维码
    def get_qr_image(self):
        folder = os.path.exists('./%s' % self.deviceid)
        if not folder:
            os.makedirs('./%s' % self.deviceid)
        else:
            pass
        res = requests.get('http://193.112.218.104:89/api?str=Initialize').text
        image = json.loads(res)['qrcode']
        data_62 = json.loads(res)['data']
        h = open("./%s/%s.jpg" % (self.deviceid, self.deviceid), "wb")
        h.write(base64.b64decode(image))
        h.close()
        os.popen('adb -s %s push ./%s/%s.jpg  /sdcard/myData/%s.jpg' % (self.deviceid, self.deviceid,  self.deviceid,self.deviceid)).read()
        time.sleep(2)
        os.popen('adb -s %s shell mv /sdcard/myData/%s.jpg /sdcard/myData/scan.jpg' % (self.deviceid, self.deviceid)).read()
        time.sleep(2)
        os.popen('adb -s %s shell curl http://127.0.0.1:8089?api=scandCode' % self.deviceid)
        time.sleep(3)
        for i in range(0, 10):
            os.popen('adb -s %s shell input tap 524 1587' % self.deviceid)
        return data_62

    def check_62(self):
        try:
            data = open('config.ini', 'r').read()
            return json.loads(data)['62'], json.loads(data)['A16']
        except:
            with open('config.ini', 'w') as f:
                f.write('{"62":"False","A16":"False"}')
            return "False", "False"

    def sys(self, ph, mm):
        self.driver.implicitly_wait(180)
        self.driver.find_elements_by_id(self.element_json[u'微信四个主按钮ID'])[0].click()
        config_data = self.check_62()
        if config_data[0] == "True":
            self.start_yz()
            if token().get_jurisdiction(TokenYZ.pdtoken(), self.deviceid) != None:
                for i in range(0, 5):
                    self.visualization('开始提62')
                    logging.info(self.deviceid + u'-开始提62')
                    data_62 = self.get_qr_image()
                    for j in range(0, 3):
                        os.system('adb -s %s shell input swipe 500 1200 500 1600' % self.deviceid)
                        self.driver.implicitly_wait(5)
                        if self.driver.find_elements_by_id('com.tencent.mm:id/co5')!= []:
                            if self.driver.find_elements_by_name('Mac 微信已登录') != []:
                                self.driver.find_element_by_name('Mac 微信已登录').click()
                                time.sleep(2)
                            if self.driver.find_elements_by_name('iPad 微信已登录') != []:
                                self.visualization('提62成功')
                                logging.info(self.deviceid + u'-提62成功')
                                print '%s----%s----%s----%s----%s\n' % (ph, mm, data_62, self.wxid, datetime.datetime.now().strftime('%Y-%m-%d'))
                                file().write('%s----%s----%s----%s----%s\n' % (ph, mm, data_62, self.wxid, datetime.datetime.now().strftime('%Y-%m-%d')), '提62成功列表.txt')
                                token().huojian_t62(self.deviceid, TokenYZ.pdtoken())
                                return data_62
                    if i == 4:
                        self.visualization('提取62失败')
                        logging.info(u'%s-提取62失败' % self.deviceid)
                        file().write('%s|\n' % ph, '提62失败列表.txt')
                        break
        if config_data[1] == "True":
            os.system('adb -s %s shell input keyevent 3' % self.deviceid)
            if token().get_jurisdiction(TokenYZ.pdtoken(), self.deviceid) != None:
                self.T_A16(ph, mm)

    def smjhy(self, ph=None, mm=None, device_token=None, hy=None):
        try:
            if self.gj_mode == '1.微霸改机'.decode("utf-8"):
                self.wechat_list = self.wb_login(ph, mm)
                if self.login_mode == '1.wxid登陆'.decode("utf-8"):
                    self.error = self.mm_login(self.wechat_list[0],self.wechat_list[1])
                if self.login_mode == '2.云码登陆'.decode("utf-8"):
                    self.error = self.zh_login(self.wechat_list)
            if self.error != None:
                self.login_fail(self.error, self.wechat_list)
            else:
                self.add_friend(self.wechat_list[0], self.wechat_list[1], hy)
                self.visualization('成功')
                logging.info(self.deviceid + u'-成功')
        except:
            try:
                self.driver.quit()
                self.visualization('失败')
                logging.info(self.deviceid + u'-失败')
            except:pass

    #发朋友圈
    def fpyq(self, ph=None, mm=None, device_token=None):
        try:
            if self.gj_mode == '1.微霸改机'.decode("utf-8"):
                self.wechat_list = self.wb_login(ph, mm)
                if self.login_mode == '1.wxid登陆'.decode("utf-8"):
                    self.error = self.mm_login(self.wechat_list[0], self.wechat_list[1])
                if self.login_mode == '2.云码登陆'.decode("utf-8"):
                    self.error = self.zh_login(self.wechat_list)
            if self.error != None:
                self.login_fail(self.error, self.wechat_list)
            else:
                self.circle_of_friends()
                self.visualization('成功')
                logging.info(self.deviceid + u'-成功')
        except:
            try:
                self.driver.quit()
                self.visualization('成功')
                logging.info(self.deviceid + u'-失败')
            except:pass
    #登录
    def wechat_signout(self, ph=None, mm=None, device_token=None):
        try:
            if self.gj_mode == '1.微霸改机'.decode("utf-8"):
                self.wechat_list = self.wb_login(ph, mm)
                if self.login_mode == '1.wxid登陆'.decode("utf-8"):
                    self.error = self.mm_login(self.wechat_list[0],self.wechat_list[1])
                if self.login_mode == '2.云码登陆'.decode("utf-8"):
                    self.error = self.zh_login(self.wechat_list)
            if self.gj_mode == '2.神奇改机'.decode("utf-8"):
                self.wechat_list = self.dd_switch(ph, mm, device_token)
                self.error = self.zh_login(self.wechat_list)
            if self.error != None:
                self.login_fail(self.error, self.wechat_list)
            else:
                self.sys(ph, mm)
                self.visualization('成功')
                logging.info(self.deviceid + u'-成功')
        except:
            try:
                self.driver.quit()
                self.visualization('失败')
                logging.info(self.deviceid + u'-失败')
            except:pass

    def T_A16(self, ph, mm):
        A16_list = []
        file_list = os.popen('adb -s %s shell ls /data/data/com.tencent.mm/files/kvcomm/'% self.deviceid).readlines()
        try:
            for _file in file_list:
                    os.system('adb -s %s shell su root chmod a+rw /data/data/com.tencent.mm/files/kvcomm/%s' % (self.deviceid,_file))
                    file_data = os.popen('adb -s %s shell su root cat -v /data/data/com.tencent.mm/files/kvcomm/%s' % (self.deviceid,_file)).read()
                    A16 = re.findall(',(A[0-9a-z]{15})', file_data)
                    if A16 != []:
                        A16_list.append(A16[0])
            device_data = os.popen('adb -s %s shell curl "http://127.0.0.1:8888/cmd?group=AppTool\&action=getHookDevice' % self.deviceid).read()
            data = json.loads(device_data)['data']
            file().write('%s|%s|%s|%s|%s|%s|%s|%s\n' % (ph, mm, A16_list[0], data['phone']['Imei'], data['build']['ANDROIDID'], data['phone']['BSSID'], data['build']['CPU_ABI'], data['build']['BRAND']), 'A16数据.txt')
            self.visualization('提A16数据成功')
            logging.info(u'%s-提A16数据成功' % self.deviceid)
            token().huojian_t62(self.deviceid, TokenYZ.pdtoken())
        except:
            self.visualization('提A16数据失败')
            logging.info(u'%s-提A16数据失败' % self.deviceid)

    def login_sys(self, ph=None, mm=None, device_token=None):
        try:
            if self.gj_mode == '1.微霸改机'.decode("utf-8"):
                self.wechat_list = self.wb_login(ph, mm)
                if self.login_mode == '1.wxid登陆'.decode("utf-8"):
                    self.error = self.mm_login(self.wechat_list[0],self.wechat_list[1])
                if self.login_mode == '2.云码登陆'.decode("utf-8"):
                    self.error = self.zh_login(self.wechat_list)
            if self.gj_mode == '2.神奇改机'.decode("utf-8"):
                self.wechat_list = self.dd_switch(ph, mm, device_token)
                self.error = self.zh_login(self.wechat_list)
            if self.error != None:
                self.login_fail(self.error, self.wechat_list)
            else:
                self.sys(ph, mm)
        except:
            try:
                self.driver.quit()
                self.visualization('失败')
                logging.info(self.deviceid + u'-失败')
            except:pass