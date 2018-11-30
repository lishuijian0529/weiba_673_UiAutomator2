# -*- coding: utf-8 -*-
import time
import logger
import logging
from OpenPhone import Open
import os
from File import file
import re
from IP_Filtering import ip_fiter
class wj():
    def __init__(self,deviceid,port):
        self.deviceid = deviceid
        self.port = port

    def start(self,m,t,filtering_mode):
        self.appPackage = re.findall('(.*?)\|', file.read('平台账号.txt')[25].strip('\n'))[0]
        self.appActivity = re.findall('\|(.*)', file.read('平台账号.txt')[25].strip('\n'))[0]
        os.system('adb -s ' + self.deviceid + ' shell am force-stop com.tencent.mm')
        driver = Open().Phone(self.appPackage, self.appActivity, self.deviceid, self.port)
        driver.implicitly_wait(60)
        while True:
            driver.find_element_by_id('org.wuji:id/exit_vpn').click()  # 切换VPN
            time.sleep(int(t))
            try:
                ip=re.findall('[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}',driver.find_element_by_id('org.wuji:id/ips').get_attribute(("text")))[0]
                logging.info(self.deviceid+u"-VPN已成功连接")
                logging.info(self.deviceid + u"-IP:%s"%ip)
                if m == '1':
                    if ip_fiter(self.deviceid,ip,filtering_mode) == True:
                        return ip
                    else:
                        pass
                if m == '2':
                    if ip_fiter(self.deviceid,ip,filtering_mode) == True:
                        return ip
                    else:
                        pass
            except:
                time.sleep(10)
