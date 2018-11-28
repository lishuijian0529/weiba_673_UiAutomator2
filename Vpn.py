# -*- coding:utf-8 -*-
import time
import logger
import logging
from OpenPhone import Open
import os
import re
from IP_Filtering import ip_fiter
class vpn():
    def __init__(self,deviceid,port):
        self.appPackage='it.colucciweb.sstpvpnclient'
        self.appActivity='it.colucciweb.sstpvpnclient.MainActivity'
        self.deviceid=deviceid
        self.port=port
    # 打开VPN
    def newvpn(self,m,t,filtering_mode):
        os.system('adb -s ' + self.deviceid + ' shell am force-stop com.tencent.mm')
        driver = Open().Phone(self.appPackage, self.appActivity, self.deviceid, self.port)
        driver.implicitly_wait(60)
        while True:
            driver.find_element_by_id('it.colucciweb.sstpvpnclient:id/start_stop').click()  # 开启VPN
            time.sleep(int(t))
            pd=driver.find_element_by_id('it.colucciweb.sstpvpnclient:id/details1').get_attribute(("text"))
            try:
                if u"(已连接)" == pd:
                    logging.info(self.deviceid+u"-VPN已成功连接")
                    try:
                        self.ip = re.findall('"cip": "([0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3})"', os.popen(
                            'adb -s ' + self.deviceid + ' shell curl "http://pv.sohu.com/cityjson"').read())[0]
                    except:
                        logging.info(self.deviceid+u'网络异常 ,请查看手机是否可以正常联网')
                    logging.info(self.deviceid + u'-' + self.ip)
                    if m == '1':
                        if ip_fiter(self.deviceid, self.ip, filtering_mode) == True:
                            return self.ip
                        else:
                            pass
                    if m == '2':
                        return self.ip
            except:pass

