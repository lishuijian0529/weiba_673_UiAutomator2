# -*- coding: utf-8 -*-
from Vpn import vpn
from File import file
import time
import logging
from wjvpn import wj
import re
from PhoneNumber import PhoneNumber
from LoginWechat import login_wechat
from Newenvironment import newenvironment
from FlightMode import flightmode
import random
import string
from OpenPhone import Open
import os
from weiba_api import WB
import json
from Server_VPS import vps
import traceback
class mode():
    # 账号注册
    def __init__(self, deviceid, port, wxmm, switchingmode ,phmode,t ,gj_mode,cooperator,country,gj,qh,login_mode,privince,filtering_mode):
        self.user = file().readuser()
        self.deviceid = deviceid
        self.wxmm = wxmm
        self.port = port
        self.switchingmode = switchingmode
        self.fm=flightmode(deviceid, port)
        self.v = vpn(self.deviceid,port)
        self.phmode = PhoneNumber(self.user[3], self.user[6], self.user[9] , self.deviceid , phmode,qh)
        self.f = phmode
        self.t = t
        self.gj_mode = gj_mode
        self.cooperator = cooperator
        self.country = country
        self.gj = gj
        self.qh = qh
        self.login_mode = login_mode
        self.privince=privince
        self.wj = wj(deviceid, port)
        self.filtering_mode = filtering_mode

    def connectbot(self):
            logging.info(self.deviceid + u'-手机暂时无网络,重新检测')
            os.system('adb -s ' + self.deviceid + ' shell am force-stop org.connectbot')
            driver = Open().Phone('org.connectbot', '.HostListActivity', self.deviceid, self.port)
            driver.implicitly_wait(180)
            driver.find_elements_by_id('android:id/icon')[0].click()
            driver.implicitly_wait(2)
            while True:
                if driver.find_elements_by_id('org.connectbot:id/console_prompt_yes') != []:
                    driver.find_element_by_id('org.connectbot:id/console_prompt_yes').click()
                    driver.find_element_by_id('android:id/content').click()
                if driver.find_elements_by_id('org.connectbot:id/console_password') != []:
                    driver.find_element_by_id('org.connectbot:id/console_password').send_keys('kk123')
                    driver.keyevent(66)
                    time.sleep(1)
                    driver.keyevent(66)
                    break
            time.sleep(3)

    def proxy(self):
        os.system('adb -s ' + self.deviceid + ' shell am force-stop org.proxydroid')
        self.driver = Open().Phone('org.proxydroid', '.ProxyDroid', self.deviceid, self.port)
        self.driver.implicitly_wait(180)
        self.driver.find_element_by_id('android:id/switchWidget').click()
        time.sleep(2)
        logging.info(self.deviceid+u'-Proxy成功连接')

    def pd_ip(self, m):
        if self.switchingmode == '1.飞行模式'.decode("utf-8"):
            return self.fm.flightmode(m,self.t,self.filtering_mode)
        if self.switchingmode == '2.VPN'.decode("utf-8"):
            return self.v.newvpn(m,self.t,self.filtering_mode)
        if self.switchingmode == '3.不换IP'.decode("utf-8"):
            self.ip =  os.popen('adb -s %s shell curl "http://ip.cip.cc'%self.deviceid).read()[0]
            return self.ip
        if self.switchingmode == '4.私人VPN'.decode('utf-8'):
            return self.wj.start(m,self.t,self.filtering_mode)
        if self.switchingmode == '5.私人VPN2'.decode('utf-8'):
            os.system('adb -s ' + self.deviceid + ' shell am force-stop com.tencent.mm')
            ip = vps(self.deviceid).switching_VPS(m, self.filtering_mode)
            logging.info(self.deviceid+u'-服务器IP地址:%s'%ip)
            while True:
                try:
                    sj_ip = os.popen('adb -s ' + self.deviceid + ' shell curl --connect-timeout 100 ip.cip.cc').read().strip('\n')
                    logging.info(self.deviceid + u'-手机IP地址:%s' % sj_ip)
                    if ip in sj_ip:
                        return ip
                    else:
                        logging.info(self.deviceid + u'-手机IP跟服务器IP不一致')
                        self.connectbot()
                        self.proxy()
                except:
                    self.connectbot()
                    self.proxy()

    def wechat_list_Verification(self,culture_list):
        if culture_list == []:
            while True:
                logging.info(self.deviceid + u'-养号列表不存在该设备号数据')
                time.sleep(12)



    def get_wechatdata(self,culture_list):
        ph = re.findall('([0-9]{1,100})_', culture_list)[0]
        logging.info(self.deviceid + u'-获取到手机号码:' + ph)
        mm = re.findall('_(.*?) ', culture_list)[0]
        logging.info(self.deviceid + u'-获取到登录密码:' + mm)
        try:
            self.device_token = re.findall('dd_cloud:(.*)',culture_list)[0]
            logging.info(self.deviceid + u'-获取到多多云码:' + self.device_token)
        except:self.device_token = 'test'
        try:
            self.hy = re.findall('ID:(.*)',culture_list)[0]
            logging.info(self.deviceid + u'-获取到好友ID:' + self.hy)
        except:self.hy = 'test'
        try:
            self.wxid ='wxid_'+re.findall('wxid_(.*)22  ', culture_list)[0]+'22'
            logging.info(self.deviceid + u'-获取WXID:' + self.wxid)
        except:
            logging.info(self.deviceid + u'-未获取到WXID')
            self.wxid = 'test'
        try:
            self.cloudCode = 'wbp:'+re.findall('wbp:(.*?)\|', culture_list)[0]
            logging.info(self.deviceid + u'-获取到云码:' + self.cloudCode)
        except:
            logging.info(self.deviceid + u'-未获取到云码')
            self.cloudCode = 'test'
        try:
            self.ip = re.findall('  ([0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3})  ', culture_list)[0]
            logging.info(self.deviceid + u'-获取到注册IP:' + self.ip)
        except:
            logging.info(self.deviceid + u'-未获取到注册IP')
            self.ip = 'test'
        try:
            self.date = re.findall('([0-9]{1,4}-[0-9]{1,2}-[0-9]{1,2})', culture_list)[0]
            logging.info(self.deviceid + u'-获取到注册日期:' + self.date)
        except:
            logging.info(self.deviceid + u'-未获取到注册日期')
            self.date = 'test'
        return ph,mm,self.device_token,self.hy,self.wxid,self.cloudCode,self.ip,self.date

    def random_password_Verification(self):
        if self.wxmm == '请输入注册密码'.decode("utf-8"):
            while True:
                keylist = ''.join([random.choice(string.digits + string.ascii_lowercase) for i in range(8)])
                if 'l' not in keylist:
                    if '9' in keylist:
                        break
            self.sjmm = keylist
            return self.sjmm
        else:
            self.sjmm = self.wxmm
            return self.sjmm

    #从养号列表获取第一条数据到微信账号数据列表去找这条数据
    def wb_mode_Verification(self):
        support_file_name = '养号列表.txt'
        support_Data = file.read(support_file_name)
        error_file_name = '登录异常账号.txt'
        error_Data_List = file.read_all(error_file_name)
        wechat_file_name = '微信账号数据.txt'
        wechat_Data_List = file.read(wechat_file_name)
        num = []
        new_data_list = []
        for data in wechat_Data_List:
            if self.deviceid in data:
                new_data_list.append(data)
        for support in support_Data:
            if 'True' not in support.strip('\n'):
                if re.findall('(.*)\|', support)[0] not in error_Data_List:
                    try:
                        for self.wechat_Data in new_data_list:
                            if re.findall('(.*)\|', support)[0] in self.wechat_Data:
                                num.append('%s|ID:%s' % (self.wechat_Data.strip('\n'), re.findall('\|(.*)', support)[0]))
                    except:
                        logging.info(self.deviceid+u'-正则没有匹配到该条数据:'+self.wechat_Data)
        if num.__len__() <> 0:
            logging.info(self.deviceid + u'设备找到%s个数据' % num.__len__())
            return num
        else:
            logging.info(self.deviceid + u'该设备在养号列表中没有数据')
            time.sleep(10000)

    def breeding_Mode(self, mode):
        culture_list = self.wb_mode_Verification()
        for culture in culture_list:
            self.pd_ip('2')
            wechat_list = self.get_wechatdata(culture)
            if mode == 'moments':
                login_wechat(deviceid=self.deviceid, port=self.port,country=None, gj_mode=self.gj_mode, wxid=wechat_list[4],
                             login_mode=self.login_mode, cloudCode=wechat_list[5],ip=wechat_list[6],date=wechat_list[7]).fpyq(ph=wechat_list[0],mm=wechat_list[1],device_token=wechat_list[2])
            if mode == 'login':
                login_wechat(deviceid=self.deviceid, port=self.port, country=None,gj_mode=self.gj_mode, wxid=wechat_list[4],
                             login_mode=self.login_mode, cloudCode=wechat_list[5],ip=wechat_list[6],date=wechat_list[7]).wechat_signout(ph=wechat_list[0],mm=wechat_list[1],device_token=wechat_list[2])
            if mode == 'addfriends':
                login_wechat(deviceid=self.deviceid, port=self.port, country=None,gj_mode=self.gj_mode, wxid=wechat_list[4],login_mode=self.login_mode, cloudCode=wechat_list[5],ip=wechat_list[6],date=wechat_list[7]).smjhy(ph=wechat_list[0],mm=wechat_list[1],device_token=wechat_list[2], hy=wechat_list[3])
            if mode == 'dlsys':
                login_wechat(deviceid=self.deviceid, port=self.port, country=None, gj_mode=self.gj_mode, wxid=wechat_list[4], login_mode=self.login_mode, cloudCode=wechat_list[5],ip=wechat_list[6],date=wechat_list[7]).login_sys(
                    ph=wechat_list[0], mm=wechat_list[1], device_token=wechat_list[2])

    #注册模式
    def Registration_Mode(self,mode):
        with open('跳辅设置.txt'.decode('utf-8'), 'r') as f:
            self.tm = json.loads(f.read())['runmode']
        while True:
            try:
                #phonenumber = '13061759881','123'
                phonenumber = self.phmode.all_getph()
                self.ip = self.pd_ip('1')
                if self.country == '2.国外'.decode("utf-8"):
                    self.wxmc = file().readwxmc().decode("gb2312").strip('\n')
                if self.country == '1.国内'.decode("utf-8"):
                    self.wxmc = file().readwxmc().decode("gb2312").strip('\n')
                self.sjmm = self.random_password_Verification()
                if mode == 'zc':
                    newenvironment(self.user[3], self.user[6], self.user[9], self.deviceid, self.port, self.user[17],self.user[20], self.sjmm, self.f, self.wxmc.strip('\n'), phonenumber, self.gj_mode,self.tm, self.cooperator, country=self.country, gj=self.gj, qh=self.qh,ip=self.ip).new_zh()
                if mode == 'zcfpyq':
                    newenvironment(self.user[3], self.user[6], self.user[9], self.deviceid, self.port, self.user[17],
                                   self.user[20], self.sjmm, self.f, self.wxmc.strip('\n'), phonenumber, self.gj_mode,self.tm, self.cooperator, country=self.country, gj=self.gj, qh=self.qh,ip=self.ip).new_zhpyq()
                if mode == 'zc_pyq_t62':
                    newenvironment(self.user[3], self.user[6], self.user[9], self.deviceid, self.port, self.user[17],self.user[20], self.sjmm, self.f, self.wxmc.strip('\n'), phonenumber, self.gj_mode,self.tm, self.cooperator, country=self.country, gj=self.gj, qh=self.qh,ip=self.ip).zc_pyq_t62()
            except:
                traceback.print_exc()
                logging.info(self.deviceid + u'-发现异常,重新注册')
                time.sleep(5)

    def zc(self):
        self.Registration_Mode('zc')

    def zcfpyq(self):
        self.Registration_Mode('zcfpyq')

    def zc_pyq_t62(self):
        self.Registration_Mode('zc_pyq_t62')

    def moments(self):
        try:
            self.breeding_Mode('moments')
        except :
            traceback.print_exc()
            logging.info(self.deviceid+u'-发现异常')

    def login(self):
        try:
            self.breeding_Mode('login')
        except:
            traceback.print_exc()
            logging.info(self.deviceid + u'-登录异常')

    def addfriends(self):
        try:
            self.breeding_Mode('addfriends')
        except:
            traceback.print_exc()
            logging.info(self.deviceid+u'-发现异常,重新切换队列')

    def dlsys(self):
        try:
            self.breeding_Mode('dlsys')
        except:
            traceback.print_exc()
            logging.info(self.deviceid+u'-发现异常,重新切换队列')

    def delete(self):
        os.popen('adb -s %s shell rm -rf /sdcard/Download/weiba/wx' % (self.deviceid))
        logging.info(self.deviceid + u'-已删除')

    def delete_wbdata(self):
        with open('微霸环境包删除设置.txt'.decode('utf-8'), 'r') as f:
            wx_data = f.readlines()
        for i in wx_data:
            try:
                os.popen('adb -s %s shell rm -rf /sdcard/Download/weiba/wx/%s.wbwx' % (self.deviceid,i.strip('\n')))
            except:pass
        logging.info('%s-设备数据删除完毕'%self.deviceid)

    def pull_weiba_data(self):
       os.popen('adb -s %s pull /sdcard/Download/weiba/wx weiba_data/%s/' % (self.deviceid, self.deviceid))

    def cloudCode_Recover(self):
            try:
                culture_list = self.wb_mode_Verification()
                accounts =json.loads(WB(self.deviceid).get_accounts())['data']
                with open('云码恢复列表.txt'.decode('utf-8'),'a') as f:
                    for i in range(0, culture_list.__len__()):
                        #取到手机号码
                        self.ph=re.findall('([0-9]{11})', culture_list[i])[0]
                        self.mm = re.findall('_(.*?) ', culture_list[i])[0]
                        self.t = re.findall('([0-9]{4}-[0-9]{2}-[0-9]{2})', culture_list[i])[0]
                        self.wxid = re.findall('wxid_(.*)22  ', culture_list[i])[0]
                        for account in accounts:
                            if self.wxid in account['strWxUUID']:
                                logging.info(self.deviceid + u'-对比结果:' + self.ph + u'存在,提取云码')
                                f.write('%s_%s  %s  %s  %s  %s|\n' % (self.ph, self.mm, self.deviceid, self.t, account['strWxUUID'], account['strCode']))
                time.sleep(10000)
            except:pass