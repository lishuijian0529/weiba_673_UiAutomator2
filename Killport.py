# -*- coding: utf-8-*-
import os
class killport():
    def kill_port(self,port):
        # 查找端口的pid
        find_port= 'netstat -aon | findstr %s' % port
        result = os.popen(find_port)
        text = result.read()
        pid= text [-5:-1]
        # 占用端口的pid
        find_kill= 'taskkill -f -pid %s' %pid
        print(find_kill)
        result = os.popen(find_kill)
        return result.read()

