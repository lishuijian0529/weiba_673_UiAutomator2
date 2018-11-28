# -*- coding: utf-8-*-
import time
import requests
import re
import logging
import TokenYZ
import json
from Token import token
from File import file
import random
import os

class PhoneNumber():
        def __init__(self, uid, password, pid, deviceid,get_phmode,qh=None):
            self.uid = uid.strip('\n')
            self.password = password.strip('\n')
            self.pid = pid.strip('\n')
            self.deviceid = deviceid
            self.get_phmode = get_phmode
            self.qh=qh
        #玉米取号
        def yumi_getphoneNumber(self):
            while True:
                try:
                    result = requests.get('http://api.jyzszp.com/Api/index/userlogin?uid=' + self.uid + '&pwd=' + self.password,timeout=10)
                    res = result.content
                    token = re.findall('[a-zA-Z0-9]{32,32}', res)
                    result = requests.get('http://api.jyzszp.com/Api/index/getMobilenum?pid=' + self.pid + '&uid=' + self.uid + '&token=' + token[0],timeout=10)
                    ph = result.content
                    sj = re.findall('[0-9]{11}',ph)[0]
                    logging.info(self.deviceid+u'-获取手机号码:'+sj)
                    if sj.__len__() == 11:
                        return sj,token[0]
                except:
                    logging.debug(u'未获取到手机号码,请确认是否卡商平台账号余额不足或卡商无号')
        #玉米发短信
        def yumi_sendmessages(self, text, sj, token):
             sendurl='http://api.jyzszp.com/Api/index/sendSms?uid='+self.uid+'&token='+token+'&pid='+self.pid+'&mobile='+sj+'&content='+ text+'+&vsendobj=10690700367'
             logging.info(self.deviceid+u'-正在发送短信'+text+u'到10690700367')
             status = re.findall('[a-z]{1,10}', requests.get(sendurl,timeout=10).content)[0]
             if status == 'succ':
                return status
             else:
                logging.info(self.deviceid + u'-发送短信回复结果:"失败",请咨询卡商')

        def yumi_cancelSMSRecv(self,ph,token):
            while True:
                url = 'http://api.jyzszp.com/Api/index/cancelSMSRecv?uid=%s&token=%s&mobiles=%s&pid=1296'%(self.uid,token,ph)
                if 'succ' in  requests.get(url).text:
                    logging.info(self.deviceid+u'-释放成功:'+ph)
                    break

        def all_getph(self):
            try:
                if self.get_phmode == "1.小鱼平台".decode('utf-8'):
                    return self.xiaoyu_get_phone()
                if self.get_phmode == "2.菜鸟平台".decode('utf-8'):
                    return self.cn_get()
                if self.get_phmode == '3.火箭API'.decode('utf-8'):
                    return self.hj_get(TokenYZ.pdtoken())
                if self.get_phmode == '4.国外私人1'.decode('utf-8'):
                    return self.get_baji_phone()
                if self.get_phmode == '5.国外私人2'.decode('utf-8'):
                    return self.get_tkt_data()
                if self.get_phmode == '6.国外私人3'.decode('utf-8'):
                    return self.gwsr3_get_ph()
                if self.get_phmode == '7.辽宁API'.decode('utf-8'):
                    return self.ln_get_ph()
                if self.get_phmode == '8.国内私人1'.decode('utf-8'):
                    while True:
                        if float(token().get_balance(TokenYZ.pdtoken()))>6.0:
                            return self.gnsr_get_ph()
                        else:
                            logging.info(self.deviceid+u'-余额不足,无法取卡,请及时充值')
                            time.sleep(10)
                if self.get_phmode == '9.老九专属API'.decode('utf-8'):
                    return self.lj_get_ph()
                if self.get_phmode == '10.国内私人2'.decode('utf-8'):
                    return self.gnsr2_get_ph()
                if self.get_phmode == '11.菜鸟国外'.decode('utf-8'):
                    return self.cn_gw_get()
                if self.get_phmode == '12.国内私人3'.decode('utf-8'):
                    return self.grsr3_get_ph()
                if self.get_phmode == '13.国内私人4'.decode('utf-8'):
                    return self.grsr4_get_ph()
                if self.get_phmode == "14.玉米平台".decode('utf-8'):
                    return self.yumi_getphoneNumber()
            except:
                logging.debug(self.deviceid+u'-未获取到手机号码,请检查是否有号可取')
                raise quit()

        #火箭获取手机号码
        def hj_get(self,token):
            while True:
                try:
                    time.sleep(random.randint(1, 10))
                    header = {'Authorization': 'Bearer ' + token}
                    result = requests.get(url='http://api.91huojian.com/card',headers = header).text
                    logging.info(self.deviceid+u'-获取到手机号码:'+re.findall('"phone":"(.*?)"',result)[0])
                    ph = re.findall('"phone":"(.*?)"', result)[0]
                    cardid = re.findall('"id":(.*?),', result)[0]
                    return ph, cardid
                except:
                    logging.info(self.deviceid+u'-获取不到手机号码')
                    time.sleep(random.randint(1, 10))
        #火箭发送短信
        def send_text(self,token,cardid,text):
            try:
                header = {'Authorization': 'Bearer ' + token}
                json1 = {'cardId': cardid, "message": text}
                res = requests.post(url='http://api.91huojian.com/card', json=json1, headers=header,timeout=100).text
                time.sleep(3)
                if json.loads(res)['code'] == '0':
                    return True
                else:
                    logging.info('%s-%s' %(self.deviceid, json.loads(res)['message']))
                    return False
            except:
                pass
        #火箭失败
        def hj_fail(self,token,cardid):
            header = {'Authorization': 'Bearer ' + token}
            requests.get('http://api.91huojian.com/card/fail?cardId=%s' % cardid, headers=header, timeout=20)

        #火箭成功
        def hj_success(self,token,cardid):
            header = {'Authorization': 'Bearer ' + token}
            requests.get('http://api.91huojian.com/card/success?cardId=%s' % cardid, headers=header, timeout=20)

        #巴基斯坦获取号码
        def get_baji_phone(self):
            while True:
                ph=requests.get('http://39.108.156.237/phone/getPhoneTel?usid=%s&type=wx&countryCode=%s' % (self.uid, self.qh)).text
                if json.loads(ph)['data']!=None:
                    logging.info(self.deviceid+u'-获取手机号码:'+json.loads(ph)['data'])
                    return json.loads(ph)['data'],'test'

        def get_baji_dx(self,ph):
            for i in range(0,100):
                try:
                    dx=requests.get('http://39.108.156.237/phone/getPhoneCode?usid=%s&phone=%s&type=wx&countryCode=%s'%(self.uid,ph,self.qh)).text
                    if json.loads(dx)['data']!=None:
                        logging.info(self.deviceid + u'-获取验证码:' + json.loads(dx)['data'])
                        return json.loads(dx)['data']
                except:
                    logging.debug(self.deviceid+u'-未获取到验证码,重新获取')
                    time.sleep(3)
        #tkt取号
        def get_tkt_data(self):
            data = file().read_TKT()
            data_new=[]
            for i in range(1,data.__len__()):
                data_new.append(data[i])
            file().delete_TKT()
            file().write_TKT(data_new)
            logging.info(self.deviceid+u'-获取到手机号码:'+re.findall('[0-9]{10}', data[0].strip('\n'))[0])
            return re.findall('[0-9]{10}', data[0].strip('\n'))[0],re.findall('\|(.*)', data[0].strip('\n'))[0]
        #tkt首次
        def get_tkt_yzm(self,ph,token):
            for i in range(0,100):
                try:
                    yzm=requests.get(token).text
                    if re.findall('([0-9]{4})',yzm)[0]!=None:
                        logging.info(self.deviceid + u'-获取验证码:'+re.findall('[0-9]{4}',yzm)[0])
                        return re.findall('[0-9]{4}',yzm)[0]
                except:
                    logging.debug(self.deviceid + u'-未获取到验证码,重新获取')
                    time.sleep(3)
                    if i==99:
                        file().write_Tkt_NotReceived('%s|%s'%(ph,token))
                        logging.info(self.deviceid + u'-已写入未收到验证码文件')

        #辽宁API取号
        def ln_get_ph(self):
            params = {"zh": (None, self.uid), "mm": (None, self.password), }
            text= requests.post(url='http://116.62.188.254/api/hqhm.php', files=params).text
            logging.info(self.deviceid+u'-获取到手机号码:'+re.findall('[0-9]{11}',text)[0])
            return re.findall('[0-9]{11}',text)[0],'test'

        #辽宁API发短信
        def ln_send(self,ph,dx):
            params = {"zh": (None, self.uid), "mm": (None, self.password), "from": (None, ph),
                      "togo": (None, '10690700367'), "content": (None, dx)}
            text = requests.post(url='http://116.62.188.254/api/fsdx.php', files=params).text
            if re.findall('"code":(.*?),',text)[0] == '10000':
                return True

        #火箭数据提交
        def qg_card_add(self, token1,ph):
            header = {'Authorization': 'Bearer ' + token1}
            res = requests.get('http://api.91huojian.com/card/add?phone=%s'%ph, headers=header)
            if res.status_code==500:
                while True:
                    logging.info(self.deviceid+u'-账户余额不足')
                    time.sleep(10)
            if json.loads(res.text)['code'] == '0':
                    logging.info(self.deviceid+u'-数据提交成功')
            if json.loads(res.text)['code'] == '1007':
                    logging.info(self.deviceid + u'-数据提交成功')
                    while True:
                        logging.info(self.deviceid+u'-现有余额不足,无法继续取卡,请及时充值')
                        if float(token().get_balance(TokenYZ.pdtoken())) > 6.0 :
                            return True
                        time.sleep(10)

        #老九API获取手机号码
        def lj_get_ph(self):
            data = file().read_lj()
            data_new = []
            for i in range(1, data.__len__()):
                data_new.append(data[i])
            file().delete_lj()
            file().write_lj(data_new)
            logging.info(self.deviceid + u'-获取到手机号码:' + data[0])
            return data[0].strip('\n'),self.pid

        #老九发短信
        def lj_send_text(self,ph,dx):
                data = {"token": (None, self.pid),
                        "from": (None, ph), "togo": (None, '10690700367'), "content": (None, dx)}
                res = requests.post('http://43.249.206.149:888/WebApi/SinglePostinfo', files=data).text
                if json.loads(res)['code'] == 10000:
                    return 'succ'
                else:
                    for i in range(0,4):
                        logging.info(self.deviceid+u'-'+json.loads(res)['message'])
                    return False

        #国内私人API'
        def gnsr_get_ph(self):
            if float(token().get_balance(TokenYZ.pdtoken())) > float(6*int(token().refresh(TokenYZ.pdtoken()))):
                data = file().read_grsr()
                data_new = []
                for i in range(1, data.__len__()):
                    data_new.append(data[i])
                file().delete_grsr()
                file().write_grsr(data_new)
                logging.info(self.deviceid + u'-获取到手机号码:' + data[0])
                return data[0].strip('\n'), 'test'
            else:
                while True:
                    logging.info(self.deviceid+u'-账户余额不足,请及时充值')
                    time.sleep(10)

        #国内私人发短信
        def gnsr_send_text(self,ph,dx):
                data = {"token": (None,'aed374ef84b162062b715080ab59cabc66abcea4c41e62083d7548080ba132210cf7dde115e721831379672bb337ec97'),
                        "from": (None, ph), "togo": (None, '10690700367'), "content": (None, dx)}
                res = requests.post('http://43.249.206.149:888/WebApi/SinglePostinfo', files=data).text
                if json.loads(res)['code'] == 10000:
                    return 'succ'
                if json.loads(res)['code'] == 10006:
                    while True:
                        logging.info(self.deviceid+u'-卡商API的账号余额不足,请及时充值')
                        time.sleep(10)
                else:
                    for i in range(0,4):
                        logging.info(self.deviceid+u'-'+json.loads(res)['message'])
                    return False

        # 国外私人3取号
        def gwsr3_get_ph(self):
            file_name = '国外私人3数据.txt'
            data = file.read(file_name)
            data_new = []
            for i in range(1, data.__len__()):
                data_new.append(data[i])
            file().delete(file_name)
            file().write(data_new,file_name)
            logging.info(self.deviceid + u'-获取到手机号码:' + re.findall('[0-9]{10}',data[0])[0])
            return re.findall('[0-9]{10}',data[0])[0], re.findall('----(.*)',data[0])[0]


        def gwsr3_send_text(self,token):
            while True:
                res = requests.get('http://119.23.42.46/getMobileSms?token=%s'%token).text
                try:
                    return re.findall('[0-9]{4}',res)[0]
                except:
                    logging.debug(self.deviceid+u'-未获取到验证码')
                    time.sleep(2)

        def gnsr2_get_ph(self):
            file_name = '国内私人2数据.txt'
            data = file.read(file_name)
            data_new = []
            for i in range(1, data.__len__()):
                data_new.append(data[i])
            file().delete(file_name)
            file().write(data_new, file_name)
            logging.info(self.deviceid + u'-获取到手机号码:' + re.findall('[0-9]{11}', data[0])[0])
            return re.findall('[0-9]{11}', data[0])[0],'test'

        def gnsr2_send(self,ph,dx):
                try:
                    res=requests.get('http://115.231.220.152:8000/sjjc/system/sendContent?phones=%s&content=%s&key=%s'%(ph,dx,self.uid)).text
                    if re.findall('"status":(.*)}',res)[0] =='1':
                        logging.info(self.deviceid+u'-发送短信发送错误，请拿着此错误信息询问卡商:%s'%res)
                        return False
                    if re.findall('"status":(.*)}',res)[0] =='2':
                        return 'succ'
                except:
                    logging.info(self.deviceid+u'-response解析失败')
        #菜鸟取号
        def cn_get(self):
            for i in range(0, 15):
                res=requests.get('http://api.jydpt.com/yhapi.ashx?Action=getPhone&token=%s&i_id=%s&d_id=&p_operator=&p_qcellcore=&mobile='%(self.uid,self.pid)).text
                if 'OK' in res:
                    logging.info(self.deviceid+u'-获取到手机号码:'+re.findall('[0-9]{11}',res)[0])
                    return re.findall('[0-9]{11}',res)[0],re.findall('OK\|(.*?)\|',res)[0]
                else:
                    time.sleep(10)
        #菜鸟发送短信
        def cn_send(self,p_id,dx):
            res=requests.get('http://api.jydpt.com/yhapi.ashx?Action=putPhoneMessage&token=%s&p_id=%s&receiver=10690700367&message=%s'%(self.uid,p_id,dx)).text
            if 'OK' in res:
                return 'succ'
            else:
                logging.info(self.deviceid+u'-%s'%res)

        def cn_lh(self,ph,p_id):
            res=requests.get('http://api.jydpt.com/yhapi.ashx?Action=phoneToBlack&token=%s&p_id=%s&i_id=1337&mobile=%s&reason=Non_hop_code'%(self.uid,p_id,ph)).text
            print res
            if 'OK' in res:
                logging.info(self.deviceid+u'-%s拉黑成功'%ph)

        def cn_get_token(self,user,pw):
            res=requests.get('http://www.xiguawto.com:18000/yhapi.ashx?Action=userLogin&userName=%s&userPassword=%s'%(user,pw)).text
            print res

        #菜鸟国外取号
        def cn_gw_get(self):
            while True:
                res=requests.get('http://api.jydpt.com/yhapi.ashx?Action=getPhone&token=%s&i_id=%s&d_id=&p_operator=&p_qcellcore=&mobile='%(self.uid,self.pid)).text
                if 'OK' in res:
                    ph=re.findall('\|([0-9]{8,100})\|', res)[0]
                    logging.info(self.deviceid+u'-获取到手机号码:'+ph)
                    return ph,re.findall('OK\|(.*?)\|',res)[0]
                else:
                    logging.info(self.deviceid+res)
                    time.sleep(10)

        def js_get(self):
            res=requests.get('http://121.43.161.165:6090/api/loginIn?name=%s&password=%s'%(self.uid,self.password)).text
            token = json.loads(res)['user']['token']

        def cn_gw_get_dx(self,p_id):
            while True:
                res=requests.get('http://api.jydpt.com/yhapi.ashx?Action=getPhoneMessage&token=%s&p_id=%s'%(self.uid,p_id)).text
                if 'OK' in res:
                    logging.info(self.deviceid+u'-获取到的验证码为:'+re.findall('\|(.*?)\|',res)[0])
                    return re.findall('\|(.*?)\|',res)[0]
                else:
                    time.sleep(2)
                    logging.debug(self.deviceid + u'-未获取到验证码,稍后两秒再试')

        # 国内私人3  Sky的
        def grsr3_get_ph(self):
            ph = requests.get(
                'http://39.108.139.162:18005/yhapi.ashx?Action=getPhone&token=%s&i_id=%s&d_id=&p_operator=&p_qcellcore=&mobile=' % (
                self.uid, self.pid)).text
            print ph

            logging.info(self.deviceid + u'-获取手机号码:' + re.findall('\|([0-9]{11})\|10690700367', ph)[0])
            return re.findall('\|([0-9]{11})\|10690700367', ph)[0], re.findall('OK\|(.*?)\|', ph)[0]

        # 国内私人3发短 Sky的
        def grsr3_send(self, p_id, dx):
            res = requests.get(
                'http://39.108.139.162:18005/yhapi.ashx?Action=putPhoneMessage&token=%s&p_id=%s&receiver=10690700367&message=%s' % (
                self.uid, p_id, dx)).text
            if 'OK' in res:
                return 'succ'
        # 国外私人3拉黑
        def grsr3_lh(self, p_id):
            res = requests.get(
                'http://39.108.139.162:18005/yhapi.ashx?Action=phoneRelease&token=%s&p_id=%s' % (
                self.uid, p_id)).text
            if 'OK' in res:
                logging.info(self.deviceid + u'-释放成功')

        def grsr4_get_ph(self):
            while True:
                try:
                    res = requests.get(
                        'http://www.xiguawto.com:18000/yhapi.ashx?Action=getPhone&token=%s&i_id=%s&d_id=&p_operator=&p_qcellcore=&mobile=' % (
                            self.uid, self.pid)).text
                    phonenumber = re.findall('\|([0-9]{11})\|10690700367', res)[0]
                    token = re.findall('OK\|(.*?)\|', res)[0]
                    data = open('手机号码过滤.txt'.decode('utf-8'), 'r').readlines()
                    list = []
                    for i in data:
                        if i.strip('\n') in phonenumber:
                            list.append(i.strip('\n'))
                    if list == []:
                        logging.info(u'%s-获取到手机号码:%s' % (self.deviceid, phonenumber))
                        return phonenumber, token
                    else:
                        logging.info(u'%s-%s被过滤' % (self.deviceid, phonenumber))
                except:
                    logging.info(u'%s-未获取到手机号码'%self.deviceid)
                    time.sleep(5)


        def grsr4_send(self, p_id, dx):
            res = requests.get(
                'http://www.xiguawto.com:18000/yhapi.ashx?Action=putPhoneMessage&token=%s&p_id=%s&receiver=10690700367&message=%s' % (
                self.uid, p_id, dx)).text
            if 'OK' in res:
                return 'succ'

        def grsr4_lh(self, p_id):
            res = requests.get(
                'http://www.xiguawto.com:18000/yhapi.ashx?Action=phoneRelease&token=%s&p_id=%s' % (
                self.uid, p_id)).text
            if 'OK' in res:
                logging.info(self.deviceid + u'-释放成功')

        def xiaoyu_get_token(self):
            try:
                res = requests.get('http://api.juxiutu.com/Api/index/userlogin?uid=%s&pwd=%s'%(self.uid,self.password)).text
                return re.findall('\|([0-9a-z]{32})',res)[0]
            except:
                logging.info(self.deviceid+u'-账号或密码错误')
                time.sleep(10000)

        def xiaoyu_get_phone(self):
            token = self.xiaoyu_get_token()
            while True:
                try:
                    self.res = requests.get(
                        'http://api.juxiutu.com/Api/index/getMobilenum?pid=%s&uid=%s&token=%s&mobile=&size=1' % (
                        self.pid, self.uid, token)).text
                    phonenumber = re.findall('([0-9]{11})\|', self.res)[0]
                    try:
                        data = open('手机号码过滤.txt'.decode('utf-8'), 'r').readlines()
                        list = []
                        for i in data:
                            if i.strip('\n') in phonenumber:
                                list.append(i.strip('\n'))
                        if list == []:
                            logging.info(u'%s-获取到手机号码:%s' % (self.deviceid, phonenumber))
                            return phonenumber, token
                        else:
                            logging.info(u'%s-%s被过滤' % (self.deviceid, phonenumber))
                    except:
                        logging.info(u'%s-获取到手机号码:%s' % (self.deviceid, phonenumber))
                        return phonenumber, token
                except:
                    logging.info('%s-%s' % (self.deviceid, self.res))
                    time.sleep(10)

        def xiaoyu_send_message(self, ph, dx):
            token = self.xiaoyu_get_token()
            res = requests.get('http://api.juxiutu.com/Api/index/sendSms?uid=%s&token=%s&pid=%s&mobile=%s&content=%s&author_uid='%(self.uid, token, self.pid, ph, dx)).text
            if 'succ' in res:
                return 'succ'
            else:
                logging.info('%s-%s' % (self.deviceid, res))

if __name__ == '__main__':
    a = PhoneNumber('295F9DEC06D34060AE766AF8E169D95C','123456', '1000', '945f3978', u'11.菜鸟国外', '213')
    #b=a.hj_get(TokenYZ.pdtoken())
    print a.grsr3_get_ph()


