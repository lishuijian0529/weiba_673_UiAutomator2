# coding=utf-8
import os
import re
import time
import xml.etree.cElementTree as ET
import logging

class Element(object):
    """
    通过元素定位,需要Android 4.0以上
    """

    def __init__(self, deviceid):
        self.deviceid = deviceid
        self.pattern = re.compile(r"\d+")

    def uidump(self):
        """
        获取当前Activity控件树
        """
        status = os.popen("adb -s %s shell uiautomator dump /sdcard/uidump.xml"%self.deviceid).read()
        if 'UI hierchary dumped' in status:
            os.popen("adb -s %s pull /sdcard/uidump.xml Elements/%s.xml"%(self.deviceid,self.deviceid))

    def __pd_element(self,attrib,name):
        """
        判断元素是否存在 
        """
        self.uidump()
        tree = ET.ElementTree(file="Elements/%s.xml" % self.deviceid)
        treeIter = tree.iter(tag="node")
        for elem in treeIter:
            if elem.attrib[attrib] == name:
                return True

    def __element(self, attrib, name):
        """
        同属性单个元素，返回单个坐标元组
        """
        if self.__pd_element(attrib,name) == True:
            tree = ET.ElementTree(file="Elements/%s.xml"%self.deviceid)
            treeIter = tree.iter(tag="node")
            for elem in treeIter:
                if elem.attrib[attrib] == name:
                    bounds = elem.attrib["bounds"]
                    coord = self.pattern.findall(bounds)
                    Xpoint = (int(coord[2]) - int(coord[0])) / 2.0 + int(coord[0])
                    Ypoint = (int(coord[3]) - int(coord[1])) / 2.0 + int(coord[1])
                    return Xpoint, Ypoint

    def __elements(self, attrib, name):
        """
        同属性多个元素，返回坐标元组列表
        """
        list = []
        if self.__pd_element(attrib, name) == True:
            tree = ET.ElementTree(file="Elements/%s.xml" % self.deviceid)
            treeIter = tree.iter(tag="node")
            for elem in treeIter:
                if elem.attrib[attrib] == name:
                    bounds = elem.attrib["bounds"]
                    coord = self.pattern.findall(bounds)
                    Xpoint = (int(coord[2]) - int(coord[0])) / 2.0 + int(coord[0])
                    Ypoint = (int(coord[3]) - int(coord[1])) / 2.0 + int(coord[1])
                    list.append((Xpoint, Ypoint))
            return list

    def findElement(self,attrib, name,t):
        """
        通过元素名称定位
        usage: findElementByName(u"相机")
        """
        while t:
            if self.__element(attrib, name) != None:
                return self.__element(attrib, name)
            else:
                time.sleep(1)

    def findElements(self,attrib, name,t):
        while t:
            if self.__elements(attrib, name) !=None:
                return self.__elements(attrib, name)
            else:
                time.sleep(1)

    def get_text(self,attrib,name):
        if self.__pd_element(attrib,name) == True:
            tree = ET.ElementTree(file="Elements/%s.xml"%self.deviceid)
            treeIter = tree.iter(tag="node")
            for elem in treeIter:
                if elem.attrib[attrib] == name:
                    return elem.attrib["text"]

class Event(object):
    def __init__(self,deviceid):
        os.popen("adb wait-for-device ")
        self.deviceid = deviceid

    def touch(self,ele,attrib,name,index=None,t=90):
        """
        触摸事件
        usage: touch(500, 500)
        """
        el=Element(self.deviceid)
        if ele == 'ele':
            d=el.findElement(attrib,name,t)
            os.popen("adb -s %s shell input tap %s %s" % (self.deviceid, d[0], d[1]))
        if ele == 'eles':
            d=el.findElements(attrib,name,t)
            i=int(index)
            os.popen("adb -s %s shell input tap %s %s" % (self.deviceid, d[i][0], d[i][1]))
        time.sleep(0.5)

    def send_key(self,text):
        """
        输入事件
        """
        os.popen('adb -s %s shell input text %s'%(self.deviceid,text))

if __name__ == '__main__':
    a=Element('945f3978').get_text('resource-id',u'com.tencent.mm:id/d74')
    if  a==u'注册':
        print '正常'
