# -*- coding:utf-8 -*-
import os
import time
import json
token = "70edbc92-2857-4c55-a4ed-ebb7ca8e3379"
while True:
    try:
        os.popen('su root screencap -p /sdcard/Download/screen.png')
        time.sleep(3)
        qr_code = os.popen(
            "su root curl -X POST \"http://www.wwei.cn/qrcode-fileupload.html?op=index_jiema\" -F \"file=@/sdcard/Download/screen.png\" " ).read()
        qr_url = json.loads(qr_code)['jiema']
        if 'weixin' in qr_url:
            task_res = os.popen('su root curl -X POST -H \"Authorization:Bearer %s\" -H \"Content-Type:application/x-www-form-urlencoded\" \"http://api.91huojian.com/task?qrcode=%s&title=WX&describe=test&expire=0&phone=\" ' % (token, qr_url)).read()
            task_id = json.loads(task_res)['data']
            for i in range(0, 200):
                os.popen('su root uiautomator dump /sdcard/Download/uidump.xml' )
                ui_data = os.popen('su root cat /sdcard/Download/uidump.xml' ).read()
                if "10690700367" in ui_data:
                    os.popen(
                        'su root curl \"http://api.91huojian.com/task/finish?taskId=%s\" -H \"Authorization:Bearer %s\" ' % (task_id, token))
                    break
    except:
        pass


