#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Colin Yao
'''用户验证程序交互'''
import os
import sys
import shelve
import random
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from conf import setting
from core.commands import Commands

class Auth_ftp(object):
    '''用户验证交互程序'''

    def __init__(self,username,user_passwd):
        '''
        构造函数
        :param username: input:username
        :param user_passwd: input:passwd
        '''
        self.user_data = {}
        self.username = username
        self.username_passwd = user_passwd
        os_res = setting.platform.system()

        if os_res == 'Windows':  #用户密码文件
            self.passwd_data_path = os.path.join('\\' + username + '\\' + username + '.' + 'dat') #使用相对路径方便迁移
            self.passwd_data = os.path.join('\\' + username + '\\' + username)
            self.file_object = os.path.join( '\\' + self.username) #默认家目录
        else:
            self.passwd_data_path = \
                os.path.join('/' + username + '/' + username + '.' + 'dat')
            self.passwd_data = \
                os.path.join('/' + username + '/' + username)
            self.file_object = os.path.join( '/' + username)
        user_obj = (self.username,self.username_passwd,self.passwd_data,random.randint(536870912, 1073741824)) # 磁盘配额512M-1024M用户名key,写入用户名密码路径磁盘配额到字典
        self.user_data[self.username] = user_obj

    def auth_user_passwd(self):
        '''
        用户验证类
        :return: True
        '''
        os_res = os.path.exists(setting.data_path+self.passwd_data_path)  # 根据用户字典文件判断用户是否存在
        if os_res !=False:
            user_file = shelve.open(setting.data_path+self.passwd_data)  # 根据返回值判断用户名密码是否验证成功
            if self.user_data[self.username][0] in user_file \
                    and  user_file[self.username][1] == self.username_passwd:
                    print("Welcome,%s,您的身份验证成功"%self.username)
                    user_file.close()
            else:
                return False
        else:
           return True

    def add_user_passwd(self):
        '''
        添加用户类
        :return:
        '''
        res = os.path.exists(setting.data_path+self.file_object)
        if res:
            print("账号信息出现问题,请联系管理员....")
        else:
            Commands(setting.data_path+self.file_object).mkdir()   # 用户账号密码文件
            Commands(setting.data_path+self.passwd_data).mkdir()   # 用户上传下载目录
            user_file = shelve.open(setting.data_path+self.passwd_data)
            user_file.update(self.user_data)
            print("用户创建成功")
            print("账号信息出现问题,请联系管理员....")