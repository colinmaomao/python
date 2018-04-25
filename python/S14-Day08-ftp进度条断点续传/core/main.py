#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Colin Yao
'''ftp客户端交互程序'''
import os
import sys
import hashlib
BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from conf import  setting
from core.auth import Auth_ftp
from core.ftp_client import Ftp_client

class Admin(object):
    '''
    admin管理类
    '''
    def run(self):
        '''
        start类
        :return:
        '''
        exit_flag = False
        print('欢迎来到ftp升级版程序,本地测试请启动server')
        def md5(user_passwd):#用户加密认证方法密码进行md5加密与服务器做验证
            md5 = hashlib.md5()
            md5.update(user_passwd.encode())
            passwd = md5.hexdigest()
            return  passwd
        menu = u'''
        \033[32;1m
        1.登陆
        2.注册
        3.退出\033[0m
        '''
        while not exit_flag:
            print(menu)
            user_option = input('请输入您的操作,输入q退出>>>:').strip()
            if user_option == '1': #登陆
                user_name = input('请输入用户名>>>:').strip()
                new_user_passwd = input('请输入您的密码>>>:').strip()
                user_passwd = md5(new_user_passwd)
                file_object = (Auth_ftp(user_name, user_passwd).passwd_data)  #传入路径变量
                res = Auth_ftp(user_name,user_passwd).auth_user_passwd()
                if res ==  None:
                    with open(setting.path_file, 'w',encoding='utf-8') as f:
                        f.write(file_object);f.close()
                    os.chdir(setting.data_path +file_object)
                    Ftp_client().link()
                elif res == False:
                    print('%s用户密码不正确' % user_name)
                else:
                    print('请先注册')

            elif user_option == '2':#注册
                user_name = input('请输入用户名>>>:').strip()
                new_user_passwd = input('请输入您的密码>>>:').strip()
                user_passwd = md5(new_user_passwd)
                user_res = Auth_ftp(user_name, user_passwd).auth_user_passwd()
                if user_res ==  None:
                    print("%s用户不需要注册"%user_name)
                    file_object = (Auth_ftp(user_name, user_passwd).passwd_data)
                    with open(setting.path_file, 'w',encoding='utf-8') as f:
                        f.write(file_object);f.close()
                    Ftp_client().link()
                elif user_res == False:
                    print("%已注册用户,密码不正确" % user_name)
                elif user_res == True:
                    Auth_ftp(user_name, user_passwd).add_user_passwd()  #创建用户名密码文件等
                    file_object = (Auth_ftp(user_name, user_passwd).passwd_data)
                    with open(setting.path_file, 'w',encoding='utf-8') as f:
                        f.write(file_object);f.close()
                    Ftp_client().link()
                else:
                    sys.exit('异常退出')

            elif user_option == 'q' or user_option == '3':
                sys.exit()
            else:
                print('输入的选项不正确,请重新输入')
