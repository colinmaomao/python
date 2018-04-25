#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Colin Yao
'''磁盘限额基础类'''
import os
import sys
BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from conf import setting

class quota(object):
    '''限额类'''
    def __init__(self,file_obj):
        '''
        构造函数
        :param file_obj: 文件名
        '''
        self.file_obj = file_obj
        self.t1_size = 0

    def directory_size(self):
        '''
        用户目录限额函数
        :return:
        '''
        rootdir = self.file_obj  # 获取当前路径
        t_size = 0
        for dirname in os.listdir(rootdir):  #获取当前路径所有文件和文件夹
            if setting.os_res == 'Windows':
                Dir = os.path.join(rootdir+'\\'+ dirname)  # 路径补齐
            elif setting.os_res == 'Linux':
                Dir = os.path.join(rootdir + '/' + dirname)  # 路径补齐
            if (os.path.isdir(Dir)):
                for r, ds, files in os.walk(Dir):
                    for file in files:  # 遍历所有文件
                        size = os.path.getsize(os.path.join(r, file))  # 获取文件大小
                        self.t1_size += size
            size = os.path.getsize(Dir)
            t_size += size
        total_size = (self.t1_size+t_size)
        return  total_size