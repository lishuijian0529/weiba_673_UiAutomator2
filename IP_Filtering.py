# -*- coding:utf-8 -*-
import logging
import logger
import re
from File import file
import sys
reload(sys)
sys.setdefaultencoding('utf8')
def ip_fiter(deviceid,ip,filtering_mode):
    if ip in file().readIpFile():
        logging.info(deviceid + u'-IP已存在,重新切换IP')
        return False
    else:
        if filtering_mode ==  '2.设定过滤IP段'.decode('utf-8'):
            filer_all=file.read('IP段设定过滤.txt')
            test=[]
            for filer_ip in filer_all:
                if filer_ip.strip('\n') in ip:
                    logging.info(deviceid + u'-被设定的IP段过滤,重新切换网络')
                    test.append(filer_ip.strip('\n'))
            if test==[]:
                file().writeIpFile(ip)
                return True
            else:
                return False
        else:
            file().writeIpFile(ip)
            return True

if __name__ == '__main__':

    print ip_fiter('213','117.63.128.134','2.设定过滤IP段')