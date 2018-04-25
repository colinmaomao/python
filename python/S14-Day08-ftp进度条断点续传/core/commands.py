#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Colin Yao
'''os命令交互'''
import os
import sys
BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from conf import setting
from src.linux_cmd_class import L_commands
from src.windows_cmd_class import W_commands

class Commands(object):
    '''命令交互类'''

    def __init__(self,file_object):
        '''
        构造函数
        :param file_object
        '''
        self.file_object=file_object

    def cd1(self):
        '''
        cd1交互函数 直接切换directors目录
        :return: res:执行结果
        '''
        if setting.os_res == 'Windows':
            res = W_commands(self.file_object).cd1()
            return res
        elif setting.os_res == 'Linux':
            res = L_commands(self.file_object).cd1()
            return res
        else:
            print('不支持此操作系统')

    def cd(self):
        '''
        cd交互函数
        :return:
        '''
        if setting.os_res =='Windows':
           res= W_commands(self.file_object).cd()
           return res
        elif setting.os_res == 'Linux':
            res=L_commands(self.file_object).cd()
            return res
        else:
            print('不支持此操作系统')

    def mkdir(self):
        '''
        mkdir:交互函数
        :return:res命令执行结果
        '''
        if setting.os_res =='Windows':
            res= W_commands(self.file_object).mkdir()
            return res
        elif setting.os_res == 'Linux':
            res=L_commands(self.file_object).mkdir()
            return res
        else:
            print('不支持此操作系统')

    def rm(self):
        '''
        rm:删除文件交互函数
        :return:res命令执行结果
        '''
        if setting.os_res == 'Windows':
            res=W_commands(self.file_object).rm()
            return res
        elif setting.os_res == 'Linux':
            res=L_commands(self.file_object).rm()
            return res
        else:
            print('不支持此操作系统')

    def drm(self):
        '''
        drm:删除目录交互函数
        :return: res命令执行结果
        '''
        if setting.os_res == 'Windows':
            res=W_commands(self.file_object).drm()
            return res
        elif setting.os_res == 'Linux':
            res=L_commands(self.file_object).drm()
            return res
        else:
            print('不支持此操作系统')

    def ls(self):
        '''
        ls:查看目录文件交互函数
        :return: res命令执行结果
        '''
        if setting.os_res == 'Windows':
            res=W_commands(self.file_object).ls()
            return res
        elif setting.os_res == 'Linux':
            res=L_commands(self.file_object).ls()
            return res
        else:
            print('不支持此操作系统')