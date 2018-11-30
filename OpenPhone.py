# -*- coding:utf-8 -*-
import re
from appium import webdriver
import os
import time

class Open():
    try:
        def Phone(self ,appPackage,appActivity,deviceid,port):
            desired_caps = {}
            desired_caps['platformName'] = 'Android'  # 设备系统
            desired_caps['automationName'] = 'UiAutomator2'
            desired_caps['platformVersion'] = os.popen('adb -s %s shell getprop ro.build.version.release' % deviceid).readlines()  # 设备系统版本
            desired_caps['deviceName'] = deviceid # 设备名称
            desired_caps['appPackage'] = appPackage
            desired_caps['appActivity'] = appActivity
            desired_caps['udid'] = deviceid
            desired_caps['unicodeKeyboard'] = "True"
            desired_caps['resetKeyboard'] = "True"
            driver = webdriver.Remote('http://localhost:'+port+'/wd/hub',desired_caps)
            return driver
    except :
        pass

if __name__ == '__main__':
    decice = '53476787'
    old_list = []
    #os.system('adb shell am start -n com.dobe.sandbox/.home.Main2Activity')
    driver = Open().Phone('com.dobe.sandbox','.home.Main2Activity', decice, '4713')
    driver.implicitly_wait(50)
    driver.find_element_by_id('com.dobe.sandbox:id/download_icon').click()
    wz = driver.find_element_by_id('com.dobe.sandbox:id/textView').get_attribute(('text'))
    print wz
    print wz == '尚未登陆,点击登陆'
    # driver.find_element_by_name('尚未登陆,点击登陆').click()
    # driver.find_element_by_id('com.dobe.sandbox:id/editText').send_keys('j007@qq.com')
    # driver.find_element_by_id('com.dobe.sandbox:id/editText2').send_keys('53084990')
    # driver.keyevent('66')
    # time.sleep(1)
    # driver.find_element_by_name('点击登陆').click()









