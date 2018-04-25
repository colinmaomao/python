#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Colin Yao
'''server端交互程序'''
import os
import sys
import time

BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from core import selectors_server
from core import select_server

class server_ftp(object):
    '''ftp_server交互程序'''
    def start(self):
        '''
        启动函数
        :return:
        '''
        print('欢迎进入Select Ftp')
        msg = '''
        1.selectors  服务端
        2.select     客户端
        3.exit       退  出
        '''
        while True:
            print(msg)
            user_choice = input('请选择操作>>>:')
            if user_choice == '1':
                server = selectors_server.selectors_ftp()
                print(time.strftime("%Y-%m-%d %X", time.localtime()), '[+]selectors server ftp already work ')
                server.start("localhost", 10000)
            elif user_choice == '2':
                server = select_server.select_ftp("localhost",10000)
                print(time.strftime("%Y-%m-%d %X", time.localtime()), '[+]select server ftp already work ')
                server.start()
            elif user_choice == '3' or user_choice== 'q'or user_choice == 'exit':
                sys.exit('程序退出')
            else:
                print('非法的操作,请重新输入')