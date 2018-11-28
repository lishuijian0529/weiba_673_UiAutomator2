# -*- coding:utf-8 -*-
import requests
import re
import os
class submissionorder():
    def submission(self,wechaturl,ph,token,expire):
        url = "http://api.91huojian.com/task"
        header = {'content-type': 'application/json','Authorization':'Bearer '+token}
        json={
            "qrcode" : wechaturl,
            "title" : "WX扫码",
            "describe" : "任务",
            "expire" : expire,
            "phone":ph
              }
        response = requests.post(url,data=None,json=json,headers=header)
        return re.findall('"data":(.*),',response.content)[0]

    def submission_hj(self,wechaturl,ph,token,expire,cardid):
        url = "http://api.91huojian.com/task"
        header = {'content-type': 'application/json','Authorization':'Bearer '+token}
        json={
            "qrcode" : wechaturl,
            "title" : "你有新的任务",
            "describe" : "点我领取任务",
            "expire" : expire,
            "phone":ph,
            "cardid":cardid
              }
        response = requests.post(url,data=None,json=json,headers=header)
        return re.findall('"data":(.*),',response.content)[0]

    def confirm(self,deviceid,taskid,token):
        cf=os.popen('adb -s %s shell curl --connect-timeout 20 -m 20 "http://api.91huojian.com/task/finish?taskId=%s" -H "Authorization:Bearer %s"'%(deviceid,taskid,token)).read()
        return re.findall('"message":"(.*)"',cf)[0]

    def fail(self,deviceid,taskid,token):
        f = os.popen('adb -s %s shell curl --connect-timeout 20 -m 20 "http://api.91huojian.com/task/fail?taskId=%s" -H "Authorization:Bearer %s"'%(deviceid,taskid,token)).read()
        return re.findall('"message":"(.*?)"',f)[0]




if __name__ == '__main__':
    print submissionorder().submission('https://weixin110.qq.com/s/346339a0f6a',ph="13033333333",token='0afb1cfc-da8b-4916-a7e1-9bb0a0048d22',expire=0)


