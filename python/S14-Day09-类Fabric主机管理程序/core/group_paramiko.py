#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Colin Yao
'''类Fabric主机管理交互程序'''
import os
import sys
import pickle
import threading
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
from conf import setting
from core  import add_machine
from model import paramiko
from core import group_sftp
from model.prettytable import PrettyTable

class fortress_main(object):
    '''fortress类'''
    def __init__(self):
        '''
        构造函数
        '''
        self.semaphore = threading.BoundedSemaphore(1)
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        with open(setting.server_list_path, 'rb') as dict_file_object:
            self.server_list_dict = pickle.load(dict_file_object)  # server_list_dict服务器字典变量
            dict_file_object.close()

    def choice(self):
        '''
        输入函数
        :return:
        '''
        add_machine.add_machine_list().view_server()
        self.group_input = input('Please input group name >>>>>>>>:')
        if self.group_input in self.server_list_dict['machine']:
            self.group_send_command()
        else:
            print('There is no group named  %s ' % self.group_input)
            self.choice()
        return self.group_input

    def ssh_group_cmd(self,command):
        '''
        组管理函数
        :return:
        '''
        for s in self.server_list_dict['machine'][self.group_input]:
            self.server_ip = self.server_list_dict['machine'][self.group_input][s]['ip']
            self.server_port = int(self.server_list_dict['machine'][self.group_input][s]['port'])
            self.server_username = self.server_list_dict['machine'][self.group_input][s]['username']
            self.server_passwd = self.server_list_dict['machine'][self.group_input][s]['passwd']
            self.ssh.connect(self.server_ip, self.server_port, self.server_username, self.server_passwd)
            self.t1 = threading.Thread(target=self.ssh_command(command))
            self.t1.setDaemon(True)
            self.t1.start()

    def ssh_connect(self,ip,port,username,passwd):
        '''
        批量激活主机函数
        :param ip:
        :param port:
        :param username:
        :param passwd:
        :return:
        '''
        self.t = threading.Thread(target=self.ssh.connect,args=(ip, port, username,passwd))#开启线程
        self.t.setDaemon(True) #设置守护线程
        self.t.start()

    def ssh_command(self,command):
        '''
        发送ssh服务器命令
        :param command:
        :return:
        '''
        stdin, stdout, stderr = self.ssh.exec_command(command)
        res, err = stdout.read(), stderr.read()  # 定义俩个变量
        self.semaphore.acquire()
        result = res if res else err  # 定义三元运算
        print((self.server_ip).center(50,'-'))
        print(result.decode())
        self.ssh.close()
        self.semaphore.release()

    def group_send_command(self):
        '''
        group发送指令函数
        :return:
\        '''
        while True:
            command_input = input('please input command,input help for help >>>>>>>>:').strip()  # 这里要调用命令
            if len(command_input) == 0:
                pass
            elif len(command_input.split()) == 1:
                if command_input == 'help':
                    self.help_page()
                elif command_input == 'exit':
                    self.ssh.close()
                    exit()
                else:
                    self.ssh_group_cmd(command_input)
            elif len(command_input.split()) >= 2:  # 命令分割
                cmd_split = command_input.split()[0]
                self.fileobject = command_input.split()[1]  # 获取文件路径
                self.filename = self.fileobject.split('/')[-1]  # 获取文件名
                if cmd_split == 'get':  #未处理
                    group_sftp.group_ftp(self.group_input,self.fileobject,self.filename).download()
                elif cmd_split == 'put':#未处理
                    group_sftp.group_ftp(self.group_input,self.fileobject,self.filename).upload()
                elif cmd_split == 'help':
                    self.help_page()
                else:
                    self.ssh_group_cmd(command_input)
            else:
                print('unsupported command')
                self.help_page()

    def help_page(self):
        '''
        help页面
        :return:
        '''
        help_page = PrettyTable(['Command.', 'Explain', ])
        help_page.add_row(['get filename', ' download file'])
        help_page.add_row(['put /path/filename', 'upload file'])
        help_page.add_row(['other', 'send command'])
        help_page.add_row(['exit ', 'exit program'])
        help_page.add_row(['help ', ''])
        print('%s' % help_page)