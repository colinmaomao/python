#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Colin Yao
'''selectclient交互程序'''
import sys
import os
import time
import platform
import random
import socket
import json

BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from conf import setting

class select_client(object):
    """FTP 客户端"""
    def __init__(self):
        '''
        构造函数
        :return:
        '''
        self.client = socket.socket()


    def start(self):
        '''
        启动函数
        :return:
        '''
        print('login time : %s' % (time.strftime("%Y-%m-%d %X", time.localtime())))
        while True:
            try:
                self.sending_msg_list = []
                self.sending_msg = input('[root@select_ftp_client]# ')
                self.sending_msg_list = self.sending_msg.split()
                self.action = self.sending_msg_list[0]
                if len(self.sending_msg_list) == 0:
                    continue
                elif len(self.sending_msg_list) == 1:
                    if self.sending_msg_list[0] == "exit":
                        print('logout')
                        break
                    else:
                        print(time.strftime("%Y-%m-%d %X", time.localtime()),
                              '-bash : %s command not found' % self.sending_msg_list[0])
                else:
                    try:
                        if platform.system() == 'Windows':
                            self.file_path = self.sending_msg_list[1]
                            self.file_list = self.sending_msg_list[1].strip().split('\\')
                            self.file_name = self.file_list[-1]
                        elif platform.system() == 'Linux':
                            self.file_path = self.sending_msg_list[1]
                            self.file_list = self.sending_msg_list[1].strip().split('/')
                            self.file_name = self.file_list[-1]
                    except IndexError:
                        pass
                    if self.action == "put":
                        self.put(self.action,self.file_name)

                    elif self.action == "get":
                        self.get(self.action,self.file_name)
                    else:
                        print(time.strftime("%Y-%m-%d %X", time.localtime()), '[+]client:-bash: %s:'
                              % self.sending_msg_list[0], 'command not found')
            except ConnectionResetError and ConnectionRefusedError and OSError and IndexError as e:
                print(time.strftime("%Y-%m-%d %X", time.localtime()), '[+]client: -bash :', e, 'Restart client')


    def put(self, action,file_name):
        '''
        客户端上传函数
        :param cmd: 上传命令
        :return:
        '''
        if os.path.exists(self.file_path) and os.path.isfile(self.file_path):
            cmd = self.action + " " + self.file_name
            self.client.send(cmd.encode())
            self.client.recv(1024).decode()
            trans_size = 0
            file_size = os.stat(self.file_path).st_size
            if file_size == 0 :
                print(time.strftime("%Y-%m-%d %X", time.localtime()), '[+]client:-bash: %s:'
                      % self.file_name, 'file not allow null')
            else:
                n = 0
                with open(self.file_path, 'rb') as f:
                    for line in f:
                        self.client.send(line)
                        trans_size += len(line)
                    else:
                        time.sleep(0.5)
                        print("\n文件上传完成。 文件大小：[%s]字节" %trans_size)
                        self.client.send(b'put done(status:200)')
        else :
            print(time.strftime("%Y-%m-%d %X", time.localtime()), '[+]client:-bash: %s:'
                  % self.file_name, 'file not found')


    def get(self,action,file_name):
        '''
        客户端下载函数
        :param cmd: 下载命令
        :return:
        '''
        cmd = self.action + " " + self.file_name
        os.chdir(setting.client_download_path)#切换到客户端下载目录
        self.client.send(cmd.encode())
        data = self.client.recv(1024)
        file_msg = json.loads(data.decode())
        file_status = file_msg['status']
        file_name = file_msg['filename']
        if file_status == 550:
            print(time.strftime("%Y-%m-%d %X", time.localtime()), '[+]client:-bash: %s:'
                  % self.file_name, 'file not found')
        elif file_status == 200:
            receive_size = 0
            file_size = file_msg['size']
            new = random.randint(1, 100000)
            n = 0
            with open(file_name+ '.'+ (str(new)), 'wb') as file_object:
                while receive_size < file_size:
                    data = self.client.recv(1024)
                    file_object.write(data)
                    receive_size += len(data)
                    file_object.flush()
                else:
                    file_object.close()
                    print(time.strftime("%Y-%m-%d %X", time.localtime()),
                          "[+]client: -bash :File get done File size is :", file_size)

    def connect(self,ip,port):
        '''
        connect ip,port
        :param ip:IP地址
        :param port:端口
        :return:
        '''
        self.client.connect((ip, port))