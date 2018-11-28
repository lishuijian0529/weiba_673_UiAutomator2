# -*- coding:utf-8 -*-
import re
import os
import logging
class analysis():
    def get(self,device):
        #return re.findall('"txt":"(.*?)",',os.popen('adb -s %s shell curl  "http://www.wwei.cn/qrcode-fileupload.html?op=index_jiema" -F "file=@/sdcard/Pictures/screen.png"'%device).read())[0]
        try:
            return re.findall('"data":"(.*?)",',os.popen('adb -s '+device+' shell curl "http://api.91huojian.com/qrcode" -F "file=@/sdcard/Pictures/succ.png"').read())[0]
        except:
            logging.info(device+u'-二维码解析失败')


if __name__ == '__main__':
    analysis().get()