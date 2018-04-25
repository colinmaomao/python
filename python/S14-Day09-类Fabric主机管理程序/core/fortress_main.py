#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Colin Yao
'''主交互程序'''
import os
import sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
from model.prettytable import PrettyTable
from core import add_machine
from core  import  group_paramiko
from core import server_paramiko

class fortress_machine(object):
    '''
    S14-Day09-类Fabric主机管理程序
    '''
    def __init__(self):
        '''
        构造方法
        '''
        pass

    def cmd_choice(self):
        '''
        帮助函数
        :return:
        '''
        cmd_choice = PrettyTable(['No.', '说明'])
        cmd_choice.add_row(['1', '组管理'])
        cmd_choice.add_row(['2', '主机管理'])
        cmd_choice.add_row(['3', '  添加server'])
        cmd_choice.add_row(['4', ' 添加group'])
        cmd_choice.add_row(['5', '  查看server'])
        cmd_choice.add_row(['6', '退出程序'])
        print(cmd_choice)

    def user_choice(self):
        '''
        用户选择函数
        :return:
        '''
        while True:
            self.cmd_choice()
            user_choice = input('Please input your choice>>>>>>:')
            if user_choice == '1':
                print('Welcome ,The list of hosts is as follows ')
                group_paramiko.fortress_main().choice()
            if user_choice == '2':
                print('Welcome ,The list of hosts is as follows ')
                server_paramiko.fortress_main().choice()
            elif user_choice == '2':
                add_machine.add_machine_list().add_server_object()
            elif user_choice == '3':
                add_machine.add_machine_list().add_add_group_object()
            elif user_choice == '4' or user_choice == 'q' or user_choice == 'exit':
                add_machine.add_machine_list().view_server()
            elif user_choice == '5' or user_choice == 'q' or user_choice == 'exit':
                sys.exit('程序退出')
            else:
                print('disallow %s please input again'%user_choice)

