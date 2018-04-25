#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Colin Yao
'''客户端交互程序'''
import os
import sys
BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from core import selectors_client
from core import select_client

class client_ftp(object):
    '''client_ftp交互类'''
    def start(self):
        '''
        启动函数
        :return:
        '''
        print('欢迎进入Select Ftp')
        msg = '''
        1.selectors模块客户端上传下载测试
        2.select客户端上传下载测试
        3.exit
        '''
        while True:
            print(msg)
            user_choice = input('请选择操作>>>:')
            if user_choice == '1':
                client = selectors_client.selectors_client()
                client.connect("localhost", 10000)
                client.start()
            elif user_choice == '2':
                client = select_client.select_client()
                client.connect("localhost", 10000)
                client.start()
            elif user_choice == '3' or user_choice == 'q' or user_choice == 'exit':
                sys.exit('程序退出')
            else:
                print('非法操作,请重新输入')