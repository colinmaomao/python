#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Colin Yao
'''windows命令基础类'''
import os
import subprocess

class W_commands(object):
    '''
    windows命令类
    '''
    def __init__(self,file_object):
        '''
        构造函数
        :param file_object:文件名
        '''
        self.cwd = os.getcwd()  # 获取当前目录
        self.file_object = [file_object] #列表文件 #取0得到文件名/或目录路径
        self.directory_object=[file_object] #目录文件
        self.file = self.file_object[0]
        self.directory = self.file_object[0]

    def cd1(self):
        '''
        切换目录
        :return:
        '''
        os.chdir(self.directory_object[0])

    def cd(self):
        '''
        #目录类
        :return:
        '''
        res= subprocess.Popen(['cd,%s' % self.directory], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.msg = res.stdout.read()
        if len(self.msg) == 0:
            self.msg = res.stderr.read()
        return self.msg

    def mkdir(self):
        '''
        创建目录类
        :return:
        '''
        res = subprocess.Popen(['md,%s' % self.directory], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.msg = res.stdout.read()
        if len(self.msg) == 0:
            self.msg = res.stderr.read()
        return self.msg

    def rm(self):
        '''
        删除文件类
        :return:
        '''
        res = subprocess.Popen(['del,%s' % self.directory], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.msg = res.stdout.read()
        if len(self.msg) == 0:
            self.msg = res.stderr.read()
        return self.msg

    def drm(self):
        '''
        删除目录类
        :return:
        '''
        res = subprocess.Popen(['rd,%s' % self.directory], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.msg = res.stdout.read()
        if len(self.msg) == 0:
            self.msg = res.stderr.read()
        return self.msg

    def ls(self):
        '''
        查看文件目录类
        :return:
        '''
        res = subprocess.Popen(['dir,%s' % self.directory], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.msg = res.stdout.read()
        if len(self.msg) == 0:
            self.msg = res.stderr.read()
        return self.msg