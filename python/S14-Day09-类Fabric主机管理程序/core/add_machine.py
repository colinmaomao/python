#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Colin Yao
'''添加主机和主机组类'''
import os
import sys
import re
import pickle
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
from conf import setting
from model.prettytable import PrettyTable

class add_machine_list(object):
    '''
    add_machine类
    '''
    def __init__(self):
        '''
        构造函数
        :param dict_file_object 字典文件
        '''
        with open(setting.server_list_path, 'rb') as dict_file_object:
            # server_list_dict服务器字典变量
            self.server_list_dict = pickle.load(dict_file_object)
            dict_file_object.close()

    def add_group_object(self):
        '''
        添加新群组新群组server字典函数
        :return:
        '''
        self.view_server()
        self.group_server_name = input('请输入要添加的组名称>>>>>>>>:')  # 组名key input 打印组内机器
        if self.group_server_name in self.server_list_dict['machine']:
            print('%s组已经存在,请重新输入...' % self.group_server_name)
            self.add_group_object()
        else:
            self.add_new_group_server(self.group_server_name)
            self.group_server_object = {self.server_name: {'ip': self.server_name, 'port': self.server_port,
                                                           'username': self.server_username,
                                                           'passwd': self.server_passwd}}  # 添加group
            self.server_list_dict['machine'][self.group_server_name] = self.group_server_object
            with open(setting.server_list_path, 'wb') as dict_file_object:
                dict_file_object.write(pickle.dumps(self.server_list_dict))
                dict_file_object.close()
        self.view_server()

    def add_server_object(self):
        '''
        添加组内server字典函数
        :return:
        '''
        self.view_server()
        self.group_server_name = input('请输入要添加server的组>>>>>>>>:')
        if self.group_server_name in self.server_list_dict['machine']:
            self.add_server(self.group_server_name)
            server_object = {'ip': self.server_name, 'port': self.server_port, 'username': self.server_username,
                             'passwd': self.server_passwd}  # 添加server
            self.server_list_dict['machine'][self.group_server_name][self.server_name] = server_object
            with open(setting.server_list_path, 'wb') as dict_file_object:
                dict_file_object.write(pickle.dumps(self.server_list_dict))
                dict_file_object.close()
            print('Server add done please check')
            self.view_server()
        else:
            print('要添加server的组%s不存在请重新输入' % self.group_server_name)
            self.add_server_object()

    def add_server(self,group_server_name):
        '''
        添加组内server函数
        :param:group_server_name: groupname
        :return:
        '''
        self.view_server()
        try:
            self.server_name = input('请输入要添加的server ip>>>>>>>>:')  # 添加server 机器
            server_name_re_rr = \
                re.compile("^(1\\d{2}|2[0-4]\\d|25[0-5]|[1-9]\\d|[1-9])\\." + "" # 判断ip正则 
                "(1\\d{2}|2[0-4]\\d|25[0-5]|[1-9]\\d|\\d)\\." + ""
                "(1\\d{2}|2[0-4]\\d|25[0-5]|[1-9]\\d|\\d)\\." + ""
                "(1\\d{2}|2[0-4]\\d|25[0-5]|[1-9]\\d|\\d)$")
            res = server_name_re_rr.findall(self.server_name)
            if res[0]: #如果有值判断是否正常
                if self.server_name not in self.server_list_dict['machine'][self.group_server_name]:
                    while True:
                        try:
                            self.server_port = input('请输入要添加的server port>>>>>>>>:')  # 判断port 1-65535
                            if int(self.server_port) >= 22 and int(self.server_port) < 65535:
                                self.server_username = input('请输入要添加的server username>>>>>>>>:')
                                self.server_passwd = input('请输入要添加的server passwd>>>>>>>>:')
                                break  # 正常取完变量后才能结束
                            else:
                                print('%s输入不正确,请输入22或22以上65535以下的数字' % self.server_port)
                        except ValueError:  # 如果出现valueerror
                            print('%s输入不正确,请输入22或22以上65535以下的数字' % self.server_port)
                else:
                    print('%s已经存在,请重新输入' % self.server_name)
                    self.add_server(self.group_server_name)
        except IndexError as e:
            print('%s输入不正确,请输入正确的ip地址'%self.server_name)
            self.add_server(self.group_server_name)

    def add_new_group_server(self,group_server_name):
        '''
        添加新组server函数
        :param group_server_name:要添加的组名
        :return:
        '''
        self.view_server()
        try:
            self.server_name = input('请输入要添加的server ip>>>>>>>>:')  # 添加server 机器
            server_name_re_rr = \
                re.compile("^(1\\d{2}|2[0-4]\\d|25[0-5]|[1-9]\\d|[1-9])\\." +""  # 判断ip正则 
                           "(1\\d{2}|2[0-4]\\d|25[0-5]|[1-9]\\d|\\d)\\." + ""
                           "(1\\d{2}|2[0-4]\\d|25[0-5]|[1-9]\\d|\\d)\\." + ""
                           "(1\\d{2}|2[0-4]\\d|25[0-5]|[1-9]\\d|\\d)$")
            res = server_name_re_rr.findall(self.server_name)
            if res[0]:  # 如果有值判断是否正常
                while True:
                    try:
                        self.server_port = input('请输入要添加的server port>>>>>>>>:')  # 判断port 1-65535
                        if int(self.server_port) >= 22 and int(self.server_port) < 65535:
                            self.server_username = input('请输入要添加的server username>>>>>>>>:')
                            self.server_passwd = input('请输入要添加的server passwd>>>>>>>>:')
                            break  # 正常取完变量后才能结束
                        else:
                            print('%s输入不正确,请输入22或22以上65535以下的数字' % self.server_port)
                    except ValueError:  # 如果出现valueerror
                        print('%s输入不正确,请输入22或22以上65535以下的数字' % self.server_port)
        except IndexError as e:
            print('%s输入不正确,请输入正确的ip地址' % self.server_name)
            self.add_server(self.group_server_name)
        self.view_server()

    def modifi_group(self, group, ip, port, username, passwd):
        '''
        修改server群组名和server群组内机器的方法,暂不做处理
        :param group:
        :param ip:
        :param port:
        :param username:
        :param passwd:
        :return:
        '''

    def view_server(self):
        '''
        查看server函数
        :return:
        '''
        view_ip = PrettyTable(['Group.', 'Ip', ])
        for i in self.server_list_dict['machine']:
            for s in self.server_list_dict['machine'][i]:
                view_ip.add_row([i, s])
        print('%s' %view_ip )