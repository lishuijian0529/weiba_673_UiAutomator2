# -*- coding: GB2312 -*-
import os
import random
import time
import sys
import logging
import logger
class file():
        @staticmethod
        def readIpFile():                       #读取IP
                try:
                        f = open(r"使用过的IP.txt", 'r')
                        s=f.read()
                        return s.splitlines()
                except Exception, e:
                        print e.message

        @staticmethod
        def  writeIpFile(ip_list):          #写入IP
                try:
                        f = '使用过的IP.txt'
                        with open(f, 'a') as f:
                                f.write(ip_list+'\n')
                except Exception, e:
                        print e.message

        @staticmethod
        def readOperationMode():#读取运行模式
                try:
                        f = open(r"运行模式.txt", 'r')
                        s = f.read().decode("gb2312")
                        return s.splitlines()
                except Exception, e:
                    print e.message

        @staticmethod
        def deletefile():#判断文件有无超过3天
                try:
                        if int(time.time()- os.path.getctime('使用过的IP.txt')) > int(259200):
                                os.remove('使用过的IP.txt')  # 删除该文件
                        else:
                                pass
                except :
                    pass

        @staticmethod
        def readuser():
                try:
                        f = open(r"平台账号.txt", 'r')
                        return f.readlines()
                except Exception, e:
                    print e.message

        @staticmethod
        def readwechatfile():
                try:
                        f = open(r"微信账号数据.txt", 'r')
                        return f.read().splitlines()
                except Exception, e:
                    print e.message

        @staticmethod
        def writewechatfile(wechat_list,file_name):
                print wechat_list
                with open(file_name.decode('utf-8'), 'a') as f:
                                f.write(u''+wechat_list)

        @staticmethod
        def sh():
                try:
                        f = open(r"朋友圈内容.txt", 'r')
                        return f.readlines()[random.randint(0, 368)].decode("gb2312")
                except Exception, e:
                        print e.message

        @staticmethod
        def readphonenumber():
                try:
                        f = open(r"手机号码.txt", 'r')
                        print f.readline()
                        return f.read().splitlines()
                except Exception, e:
                        print e.message

        @staticmethod
        def writephonenumber(Phonenumber):
                try:
                        wechatfile = "手机号码.txt"
                        with open(wechatfile, 'w') as f:
                                for i in range(0,Phonenumber.__len__()):
                                        f.write(Phonenumber[i] + "\n")
                except Exception, e:
                    print e.message


        @staticmethod
        def readwxmc():
                try:
                        f = open(r"微信名称.txt", 'r')
                        wxmc=f.readlines()
                        return wxmc[random.randint(0, wxmc.__len__())]
                except Exception, e:
                    print e.message

        @staticmethod
        def readerrorph():
                try:
                        f = open(r"加好友成功列表.txt", 'r')
                        return f.read().splitlines()
                except Exception, e:
                    print e.message

        @staticmethod
        def writehy(sj):
                try:
                        wechatfile = "加好友成功列表.txt"
                        with open(wechatfile, 'a') as f:
                                f.write(sj+'\n')
                except Exception, e:
                    print e.message

        @staticmethod
        def readtoken():
                try:
                        f = open(r"tcl85.ini", 'r')
                        return f.read().splitlines()
                except Exception, e:
                        print e.message

        @staticmethod
        def writetoken(token):
                try:
                        try:os.remove('tcl85.ini')
                        except:pass
                        f = open("tcl85.ini", 'w')  # 新建该文件
                        f.write(token)
                except Exception, e:
                    print e.message

        @staticmethod
        def write_friend_fail(text):
                try:
                        file='加好友异常.txt'
                        with open(file,'a') as file:
                            file.write(text+'\n')
                except Exception, e:
                    print e.message

        @staticmethod
        def write_pyq_fail(text):
                try:
                        file='发朋友圈异常.txt'
                        with open(file,'a') as file:
                            file.write(text+'\n')
                except Exception, e:
                    print e.message

        @staticmethod
        def write_pyq_succ(text):
                try:
                        file = '养号成功列表.txt'
                        with open(file, 'a') as file:
                                file.write(text + '\n')
                except Exception, e:
                        print e.message

        @staticmethod
        def read_culture_list():
                try:
                        file = '养号列表.txt'
                        with open(file,'r') as file:
                                return file.readlines()
                except:pass

        @staticmethod
        def t62_write(list_data):
                try:
                        file = '提62成功列表.txt'
                        with open(file,'a') as file:
                                file.write(list_data+'\n')
                except:pass
        @staticmethod
        def writetmp(list):
                try:
                        try:
                                open('tmp.ini','r').read()
                                open('tmp.ini', 'w')
                        except:
                                open('tmp.ini', 'w')
                        with open('tmp.ini','a')as f:
                                for i in list:
                                        reload(sys)
                                        sys.setdefaultencoding("utf-8")
                                        f.write(i+'\n')
                except:pass

        @staticmethod
        def readtmp():
                try:
                        with open('tmp.ini','r') as f:
                                return f.readlines()
                except:return None


        @staticmethod
        def write_culture_list(list):
                file='云码恢复列表.txt'
                with open(file,'a') as f:
                        f.write(list+'\n')

        @staticmethod
        def wrtie_yh_list(list):
                file='养号列表.text'
                with open(file,'r')as f:
                        f.write(list+'\n')

        @staticmethod
        def read_TKT():
                with open('TKT数据.txt', 'r')as f:
                       return f.readlines()

        @staticmethod
        def delete_TKT():
                os.remove('TKT数据.txt')

        @staticmethod
        def write_TKT(data):
                with open('TKT数据.txt', 'a') as f:
                        for i in range(0,data.__len__()):
                                f.write(data[i])

        @staticmethod
        def write_Tkt_NotReceived(data):
                with open('TKT未收到验证码.txt','a')as f:
                        f.write(data+'\n')

        @staticmethod
        def wite_Tkt_NotHopCode(data):
                with open('TKT未跳码.txt','a')as f:
                        f.write(data+'\n')

        @staticmethod
        def write_Tkt_gw(data):
            with open('国外微信数据.txt','a')as f:
                f.write(data+'\n')

        @staticmethod
        def read_lj():
                with open('老九专属数据.txt','r')as f:
                        return f.readlines()

        @staticmethod
        def delete_lj():
                os.remove('老九专属数据.txt')

        @staticmethod
        def write_lj(data):
                with open('老九专属数据.txt', 'a') as f:
                        for i in range(0,data.__len__()):
                                f.write(data[i])

        @staticmethod
        def wite_lj_NotHopCode(data):
                with open('老九未跳码.txt','a')as f:
                        f.write(data+'\n')

        @staticmethod
        def read_grsr():
                with open('国内私人数据.txt', 'r')as f:
                        return f.readlines()

        @staticmethod
        def delete_grsr():
                os.remove('国内私人数据.txt')

        @staticmethod
        def write_grsr(data):
                with open('国内私人数据.txt', 'a') as f:
                        for i in range(0, data.__len__()):
                                f.write(data[i])

        @staticmethod
        def read(file_name):
                with open(file_name.decode('utf-8'), 'r')as f:
                        return f.readlines()

        @staticmethod
        def delete(file_name):
                os.remove(file_name.decode('utf-8'))

        @staticmethod
        def write(data,file_name):
                with open(file_name.decode('utf-8'), 'a') as f:
                        for i in range(0, data.__len__()):
                                f.write(data[i])

        @staticmethod
        def write_NotHopCode(data,file_name):
                with open(file_name.decode('utf-8'), 'a')as f:
                        f.write(data + '\n')

        @staticmethod
        def read_all(file_name):
                with open(file_name.decode('utf-8'), 'r')as f:
                        return f.read()


