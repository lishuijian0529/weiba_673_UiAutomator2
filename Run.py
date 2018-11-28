# -*- coding:utf-8 -*-
import logging
import os
from Appium import AppiumServer
import tkinter as tk
from tkinter import ttk
from Mode import mode
import time,threading
import TokenYZ
from Token import token
from File import file

def run(xz,port,bport,deviceid,switch_ip,password,phmode,t,gj_mode,chvarUn,country,gj,qh,login_mode,privince,filtering_mode):
    AppiumServer().start_AppiumS(port, bport)
    time.sleep(15)
    rm = mode(deviceid, port,password,switch_ip,phmode,t,gj_mode,chvarUn,country,gj,qh,login_mode,privince,filtering_mode)
    if "1.注册模式".decode("utf-8") == xz:
        logging.info(u"-进入账号注册")
        rm.zc()
    if "2.注册发朋友圈".decode("utf-8") == xz:
        logging.info(u"-进入账号注册+发朋友圈模式")
        rm.zcfpyq()
    if "3.登录发朋友圈".decode("utf-8") == xz:
        logging.info(u"-进入发文字朋友圈模式")
        rm.moments()
    if "4.登录提62(仅支持国内)".decode("utf-8") == xz:
        logging.info(u"-进入登录账号提62")
        rm.login()
    if "5.加好友".decode("utf-8") == xz:
        logging.info(u"-进入加好友模式")
        rm.addfriends()
    if '7.删除微霸数据'.decode("utf-8") == xz:
        logging.info(u"-删除微霸数据模式")
        rm.delete()
    if '8.删除指定微霸数据'.decode("utf-8") == xz:
        logging.info(u"-删除指定微霸数据模式")
        rm.delete_wbdata()
    if '9.微霸数据提取'.decode("utf-8") == xz:
        rm.pull_weiba_data()
    if '10.云码数据恢复到文本'.decode("utf-8") == xz:
        logging.info(u"-开始恢复云码")
        rm.cloudCode_Recover()
    if '11.注册发圈提62'.decode("utf-8") == xz:
        logging.info(u"-注册发圈提62")
        rm.zc_pyq_t62()
    if '12.登陆扫一扫'.decode('utf-8') == xz:
        logging.info(u"-登陆扫一扫")
        rm.dlsys()
def select_device():
    devices = os.popen('adb devices').read().splitlines()
    device_list = []
    for i in range(1, devices.__len__()):
        if 'device' in devices[i]:
            if 'List' not in devices[i]:
                device_list.append(devices[i][:-7])
    return device_list

def pdxc(xz,switch_ip,password,phmode,t,gj_mode,chvarUn,country,gj,qh,login_mode,privince,filtering_mode):
    device_list = select_device()
    time.sleep(2)
    jg=TokenYZ.dlyz()
    if jg == None:
        logging.info(u"-第一次运行")
        xcs=TokenYZ.xrtoken()
        logging.info(u"-可运行线程数:%s"%xcs)
        if int(xcs)>= int(device_list.__len__()):
            for i in range(0,device_list.__len__()):
                time.sleep(5)
                threading.Thread(target=run, args=(xz, str(i+4732), str(i+4832), (device_list[i]), switch_ip, password, phmode, t, gj_mode, chvarUn, country, gj, qh, login_mode, privince, filtering_mode)).start()
        else:
            logging.info(u"-连接的手机数量已超过线程数" )
            time.sleep(10000)
    else:
        jg=TokenYZ.pdsb()
        if jg == '1':
            logging.info(u"-已经绑定该设备")
            xcs = token().get_me(TokenYZ.pdtoken())['data']['maxThreadNum']
            logging.info(u"-可运行线程数:%s"%xcs)
            if int(xcs) >= int(device_list.__len__()):
                for i in range(0, device_list.__len__()):
                    time.sleep(5)
                    threading.Thread(target=run, args=(xz, str(i + 4732), str(i + 4832), (device_list[i]), switch_ip, password, phmode, t, gj_mode, chvarUn, country, gj, qh, login_mode, privince, filtering_mode)).start()
            else:
                logging.info(u"-连接的手机数量已大于线程数")
                time.sleep(10000)
        if jg == '0':
            logging.info(u"-已经绑定过设备,请在原设备运行脚本")
            time.sleep(10000)

def qd():
    os.system("start taskkill /f /t /im node.exe")
    device_list = select_device()
    win = tk.Tk()
    win.iconbitmap('1.ico')
    win.title("火箭注册v3.7.1.1")  # 在这里修改窗口的标题
    ttk.Label(win, text='已连接设备:%s' %device_list, anchor='c').grid(row=1)
    ttk.Label(win, text='', anchor='c').grid(row=2)
    ttk.Label(win, text='本程序仅供技术交流、请勿用于商业或非法用途', anchor='c').grid(row=3)
    ttk.Label(win, text='如产生法律纠纷与本程序无关', anchor='c').grid(row=4)
    ttk.Label(win, text='如确认不用于商业或非法用途则', anchor='c').grid(row=5)
    ttk.Label(win, text='请点击"确定",否则请点击退出本程序', anchor='c').grid(row=6)
    ttk.Label(win, text='', anchor='c').grid(row=9)
    ttk.Label(win, text='', anchor='c').grid(row=7)
    action = ttk.Button(win, text="确 定", command=win.quit)
    action.grid( row=200)
    password = ttk.Entry(win, width=29, textvariable=tk.StringVar())
    if file.readtmp() != None:
        password.insert(0,file.readtmp()[0].strip('\n'))
    else:
        password.insert(0, '请输入注册密码')
    password.grid(column=0, row=9)
    ip_mode = ttk.Combobox(win, width=27, textvariable=tk.StringVar(), state='readonly')
    ip_mode['values'] = ('1.飞行模式', '2.VPN', '3.不换IP', '4.私人VPN', '5.私人VPN2')
    run_mode = ttk.Combobox(win, width=27, textvariable=tk.StringVar(), state='readonly')
    run_mode['values'] = ('1.注册模式', '2.注册发朋友圈', '3.登录发朋友圈', '4.登录提62(仅支持国内)','5.加好友', '6.注册模式(仅支持国外720*1280)', '7.删除微霸数据', '8.删除指定微霸数据','9.微霸数据提取','10.云码数据恢复到文本','11.注册发圈提62','12.登陆扫一扫')
    run_mode.grid(row=10)
    run_mode.current(0)
    login_mode=ttk.Combobox(win, width=27, textvariable=tk.StringVar(), state='readonly')
    login_mode['values'] = ('1.wxid登陆','2.云码登陆')
    login_mode.grid(row=11)
    login_mode.current(0)
    ip_mode.grid(row=12)
    ip_mode.current(0)
    phmode = ttk.Combobox(win, width=27, textvariable=tk.StringVar(), state='readonly')
    phmode['values'] = ['1.小鱼平台','2.菜鸟平台','3.火箭API','4.国外私人1','5.国外私人2','6.国外私人3','7.辽宁API','8.国内私人1','9.老九专属API','10.国内私人2','11.菜鸟国外','12.国内私人3','13.国内私人4','14.玉米平台']
    phmode.grid(row=13)
    phmode.current(0)
    t = ttk.Entry(win, width=29, textvariable=tk.StringVar())
    if file.readtmp() != None:
        t.insert(0,file.readtmp()[1].strip('\n'))
    else:
        t.insert(0, '10')
    t.grid(column=0, row=17)
    gj_mode = ttk.Combobox(win, width=27, textvariable=tk.StringVar(), state='readonly')
    gj_mode['values'] = ['1.微霸改机','2.神奇改机','测试']
    gj_mode.grid(row=14)
    gj_mode.current(0)
    cooperator = ttk.Combobox(win, width=27, textvariable=tk.StringVar(), state='readonly')
    cooperator['values'] = ['1.火箭辅助', '2.秒辅辅助']
    cooperator.grid(row=15)
    cooperator.current(0)
    country = ttk.Combobox(win, width=27, textvariable=tk.StringVar(), state='readonly')
    country['values'] = ['1.国内', '2.国外']
    country.grid(row=16)
    country.current(0)
    gj = ttk.Entry(win, width=29, textvariable=tk.StringVar())
    if file.readtmp() != None:
        gj.insert(0,file.readtmp()[2].strip('\n'))
    else:
        gj.insert(0, '请输入国家(仅国外)')
    gj.grid(column=0, row=18)
    qh = ttk.Entry(win, width=29, textvariable=tk.StringVar())
    if file.readtmp() != None:
        qh.insert(0,file.readtmp()[3].strip('\n'))
    else:
        qh.insert(0, '请输入区号(仅国外)')
    qh.grid(column=0, row=19)
    privince= ttk.Entry(win, width=29, textvariable=tk.StringVar())
    privince.insert(0, '请输入省份,仅专属API')
    privince.grid(column=0, row=20)
    fm = ttk.Combobox(win, width=27, textvariable=tk.StringVar(), state='readonly')
    fm['values'] =['1.不设定过滤IP段', '2.设定过滤IP段']
    fm.grid(row=21)
    fm.current(0)
    win.mainloop()
    list=[]
    list.append(password.get())
    list.append(t.get())
    list.append(gj.get())
    list.append(qh.get())
    file.writetmp(list)
    pdxc(run_mode.get(),ip_mode.get(),password.get(),phmode.get(),t.get(),gj_mode.get(),cooperator.get(),country.get(),gj.get(),qh.get(),login_mode.get(),privince.get(),fm.get())

if __name__ == '__main__':
    qd()


