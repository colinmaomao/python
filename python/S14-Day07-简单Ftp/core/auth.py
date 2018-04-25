#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Colin Yao
import os,sys,shelve
BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR) #添加环境变量
from conf import  setting
from src.auth_class import Auth
from core.commands import  Commands

class Auth_ftp(object):
    def __init__(self,username,user_passwd):
        self.user_data = {}
        self.username = username   #用户名
        self.username_passwd = user_passwd  #密码
        os_res = setting.platform.system()
        if os_res == 'Windows':    #用户密码文件
            self.passwd_data_path = os.path.join(setting.data_path
                                                 + '\\'+ username +  '\\'+ username + '.' + 'dat') #Windows用户密码文件路径
            self.passwd_data = os.path.join(setting.data_path + '\\' + username+ '\\' + username)  # Windows用户密码文件
            self.file_object = os.path.join(setting.data_path + '\\' + self.username)
        else:
            self.passwd_data_path = \
                os.path.join(setting.data_path + '/' + username  + '/' + username + '.' + 'dat')  # Linux用户密码文件路径
            self.passwd_data = \
                os.path.join(setting.data_path + '/' + username  + '/' + username)  # Linux用户密码文件
            self.file_object = os.path.join(setting.data_path + '/' + username)

        user_obj = (self.username,self.username_passwd,self.passwd_data) # '''用户名作为key,把用户名,密码,目录,写到字典中方便调用'''
        self.user_data[self.username] = user_obj

    '''验证用户是否存在'''
    def auth_user_passwd(self):
        '''判断文件路径是否存在然后返回用户是否存在'''
        os_res = os.path.exists(self.passwd_data_path)
        if os_res !=False:
            user_file = shelve.open(self.passwd_data)
            if self.user_data[self.username][0] in user_file\
                and  user_file[self.username][1] == self.username_passwd:
                    print("Welcome,%s,您的身份验证成功"%self.username)
                    user_file.close()
            else:
                return False
        else:
           return True

    def add_user_passwd(self):
        res = os.path.exists(self.file_object)
        if res != True:
            Commands(self.file_object).mkdir() #用户账号密码文件
            Commands(self.passwd_data).mkdir()  #用户上传下载目录
            user_file = shelve.open(self.passwd_data)
            user_file.update(self.user_data)
            print("用户创建成功")
        else:
            print("账号信息出现问题,请联系管理员....")

