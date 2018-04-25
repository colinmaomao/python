#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Colin Yao
'''linux命令基础类'''
import os
import subprocess

class L_commands(object):
    '''linux命令类'''
    def __init__(self,file_object):
        '''
        构造函数
        :param file_object:
        '''
        self.cwd = os.getcwd()
        self.file_object = [file_object]
        self.directory_object=[file_object]
        self.file = self.file_object[0]
        self.directory = self.file_object[0]

    def cd1(self):
        '''
        cd1切换目录类
        :return:
        '''
        os.chdir(self.directory_object[0])

    def cd(self):
        '''
        cd目录类
        :return:
        '''
        res = subprocess.Popen(['cd %s' % self.directory], shell=True, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        self.msg = res.stdout.read()
        if len(self.msg) == 0:
            self.msg = res.stderr.read()
        return self.msg

    def mkdir(self):
        '''
        创建目录类
        :return:
        '''
        res = subprocess.call(['mkdir -p %s' % self.directory], shell=True, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
        self.msg = res.stdout.read()
        if len(self.msg) == 0:
            self.msg = res.stderr.read()
        return self.msg

    def rm(self):
        '''
        删除文件类
        :return:
        '''
        res = subprocess.call(['rm -f %s' % self.directory], shell=True, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
        self.msg = res.stdout.read()
        if len(self.msg) == 0:
            self.msg = res.stderr.read()
        return self.msg

    def drm(self):
        '''
        删除目录类
        :return:
        '''
        res = subprocess.call(['rm -rf %s' % self.directory], shell=True, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
        self.msg = res.stdout.read()
        if len(self.msg) == 0:
            self.msg = res.stderr.read()
        return self.msg

    def ls(self):
        '''
        文件查看类
        :return:
        '''
        res = subprocess.call(['ls -l %s' % self.directory], shell=True, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
        self.msg = res.stdout.read()
        if len(self.msg) == 0:
            self.msg = res.stderr.read()
        return self.msg