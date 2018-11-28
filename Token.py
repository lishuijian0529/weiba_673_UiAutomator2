# -*- coding:utf-8 -*-
import requests
import re
from File import file
import os
import logging
import logger
import json
class token:
    def get(self,username,password):
        url = 'http://passport.91huojian.com/auth'
        # 获取token
        json1={"username":username,"password":password }
        header = {"Content-Type":"application/json","Accept":"application/json"}
        response = requests.post(url=url,headers=header,json=json1).text
        return json.loads(response)['token'],json.loads(response)['maxThreadNum']

    def check(self,token):
        url = 'http://passport.91huojian.com/check'
        header = {'Authorization': 'Bearer ' +token}
        response = requests.get(url,data=None, json=None, headers=header)
        return response.status_code

    def refresh(self,token):
        url = 'http://passport.91huojian.com/refresh'
        header = {'Authorization': 'Bearer ' + token}
        response = requests.get(url,data=None,json=None,headers=header)
        if response.status_code == 200:
            jg=json.loads(response.text)['token']
            xc=json.loads(response.text)['maxThreadNum']
            b = re.findall(': (.*)', os.popen('ipconfig /all').read().splitlines()[3])[0]
            file().writetoken(jg+ b[2] + b[4])
            return xc

    def get_balance(self,token):
        url = 'http://api.91huojian.com/user/demander/me'
        header = {'Authorization': 'Bearer ' + token}
        balance = re.findall('"balance":(.*?),',requests.get(url,data=None,json=None,headers=header).text)[0]
        return balance

    def huojian_t62(self,device,token):
        url = 'http://api.91huojian.com/order/62'
        header = {'Authorization': 'Bearer' + token}
        res = requests.get(url=url,headers=header).text
        if '1002' ==json.loads(res)['code']:
            logging.info(device+u'该账号没有权限提62')
            return False
        if '1007' ==json.loads(res)['code']:
            logging.info(device+u'该账号余额不足')
            return False
        if '0' ==json.loads(res)['code']:
            return True
        else:
            return False

    def get_jurisdiction(self, token, deviceid):
        url = 'http://api.91huojian.com/user/demander/me'
        header = {"Authorization":"Bearer " + token}
        response = requests.get(url=url, headers=header).text
        if json.loads(response)['data']['balance'] > 1:
            if json.loads(response)['data']['price62'] != -1:
                return True
            else:
                logging.info(u'%s-此账号没有提62权限' % deviceid)
        else:
            logging.info(u'%s-账号余额低于1元,请充值后再提62' % deviceid)

    def get_me(self,token):
        url = 'http://api.91huojian.com/user/demander/me'
        header = {'Authorization': 'Bearer ' + token}
        return json.loads(requests.get(url, data=None, json=None, headers=header).text)

if __name__ == '__main__':

    token1=token().get_me('00977409-b4ab-4c99-83cc-569eb4eb641e')
    print token1['data']['maxThreadNum']



