# -*- coding: utf-8 -*-
import os
from File import file
import re
from Token import token
import logging
def xrtoken():
    """
            写入加密token
                    """
    b = re.findall(': (.*)', os.popen('ipconfig /all').read().splitlines()[3])[0]
    user = file().readuser()
    try:
        tk = token().get(user[17].strip('\n'), user[20].strip('\n'))
        print tk
        file().writetoken(tk[0] + b[2] + b[4])
        return tk[1]
    except:
        logging.info(u'账号脚本可允许数量超过限制')


def dlyz():
    """
        判断程序是否第一次运行
                """
    token = file().readtoken()
    return token

def gettoken():
    """
    获取原始token
            """
    token = file().readtoken()
    return token[0][:-2]

def pdsb():
    """
       判断设备
               """
    b = re.findall(': (.*)', os.popen('ipconfig /all').read().splitlines()[3])[0]
    token1 = b[2]+b[4]
    token2 = file().readtoken()[0][-2:]
    if token1 == token2:
        return '1'
    else:
        return '0'


def pdtoken():
    """
        判断token是否有效
                """
    token1=gettoken()
    jg=token().check(token1)
    if jg == 401:
        token().refresh(token1)
        return gettoken()
    if jg == 200:
        return gettoken()


if __name__ == '__main__':
    print pdtoken()