#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Colin Yao
import os,sys,platform
BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR) #添加环境变量
from conf import setting
from src.linux_cmd_class import L_commands
from src.windows_cmd_class import W_commands


class Commands(object):
    def __init__(self,file_object):
        self.file_object=file_object

    def cd1(self):
        if setting.os_res == 'Windows':
            res = W_commands(self.file_object).cd1()
            return res
        elif setting.os_res == 'Linux':
            res = L_commands(self.file_object).cd1()
            return res
        else:
            print('不支持此操作系统')

    '''进入目录'''
    def cd(self):
        if setting.os_res =='Windows':
           res= W_commands(self.file_object).cd()
           return res
        elif setting.os_res == 'Linux':
            res=L_commands(self.file_object).cd()
            return res
        else:
            print('不支持此操作系统')

    '''创建目录'''
    def mkdir(self):
        if setting.os_res =='Windows':
            res= W_commands(self.file_object).mkdir()
            return res
        elif setting.os_res == 'Linux':
            res=L_commands(self.file_object).mkdir()
            return res
        else:
            print('不支持此操作系统')


    '''删除文件'''
    def rm(self):
        if setting.os_res == 'Windows':
            res=W_commands(self.file_object).rm()
            return res
        elif setting.os_res == 'Linux':
            res=L_commands(self.file_object).rm()
            return res
        else:
            print('不支持此操作系统')

    '''删除目录'''
    def drm(self):
        if setting.os_res == 'Windows':
            res=W_commands(self.file_object).drm()
            return res
        elif setting.os_res == 'Linux':
            res=L_commands(self.file_object).drm()
            return res
        else:
            print('不支持此操作系统')
