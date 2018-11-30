# -*- coding:utf-8 -*-
import paramiko
import json
from File import file
import re
import logging
import logger
import time
from IP_Filtering import ip_fiter
class vps():
    def __init__(self,deviceid):
        self.deviceid=deviceid
        self.vps_data = file.read_all('VPS.json')
        for dev in json.loads(self.vps_data):
            if self.deviceid == dev['deviceid']:
                self.vps= dev
                break
        #try:
        #    print self.vps
        #except:
        #    while True:
        #        logging.info(self.deviceid + u'-VPS.json文件中未配置%s设备的数据,请配置好所有连接上的设备数据再运行'%self.deviceid)
        #        time.sleep(10)

    def login(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.vps['hostname'], port=int(self.vps['port']), username=self.vps['username'],
                    password=self.vps['password'])
        return ssh

    def switch(self):
        ssh=self.login()
        logging.info(self.deviceid+u'-断开连接')
        ssh.exec_command('%s' % self.vps['disconnect_command'] )
        time.sleep(2)
        logging.info(self.deviceid + u'-开始拨号')
        ssh.exec_command('%s' % self.vps['connection_command'])
        time.sleep(10)
        stdin, stdout, stderr = ssh.exec_command('curl --connect-timeout 100 ip.cip.cc')
        ip = stdout.read()
        logging.info(self.deviceid + u'-连接成功')
        return ip

    def switching_VPS(self,m,filtering_mode):
        while True:
            try:
                server_res = self.switch().strip('\n')
                ip = re.findall('[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}', server_res)
                if ip != []:
                    if m == '1':
                        if ip_fiter(self.deviceid,ip[0],filtering_mode) == True:
                            return ip[0]
                        else:
                            pass
                    if m == '2':
                        file().writeIpFile(ip[0])
                        return ip[0]
            except:
                logging.info(self.deviceid + u'-服务器暂时无法联网,尝试重新拨号')


