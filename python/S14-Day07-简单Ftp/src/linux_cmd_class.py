#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Colin Yao
import os,sys,subprocess
class L_commands(object):
    def __init__(self,file_object):
        self.cwd = os.getcwd()  # 获取当前目录
        self.file_object = [file_object] #列表文件 #取0得到文件名/或目录路径
        self.directory_object=[file_object] #目录文件
        self.file = self.file_object[0]
        self.directory = self.file_object[0]

    def cd1(self):
        os.chdir(self.directory_object[0])

    '''进入目录'''
    def cd(self):
        res = subprocess.Popen(['cd %s' % self.directory], shell=True, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        self.msg = res.stdout.read()
        if len(self.msg) == 0:
            self.msg = res.stderr.read()
        return self.msg

    '''创建目录'''
    def mkdir(self):
        res = subprocess.call(['mkdir -p %s' % self.directory], shell=True, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
        self.msg = res.stdout.read()
        if len(self.msg) == 0:
            self.msg = res.stderr.read()
        return self.msg


    '''删除文件'''
    def rm(self):
        res = subprocess.call(['rm -f %s' % self.directory], shell=True, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
        self.msg = res.stdout.read()
        if len(self.msg) == 0:
            self.msg = res.stderr.read()
        return self.msg

    '''删除目录'''
    def drm(self):
        res = subprocess.call(['rm -rf %s' % self.directory], shell=True, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
        self.msg = res.stdout.read()
        if len(self.msg) == 0:
            self.msg = res.stderr.read()
        return self.msg
