#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Colin Yao

import os
import sys
import json
import time
import random
import socket
import platform
BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from conf import setting


class selectors_client(object):
    """FTP 客户端"""
    def __init__(self):
        '''
        构造函数
        :param
        :return
        '''
        self.client = socket.socket()

    def start(self):
        '''
        启动函数
        :param:
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
                        self.put()
                    elif self.action == "get":
                        self.get()
                    else:
                        print(time.strftime("%Y-%m-%d %X", time.localtime()),'[+]client:-bash: %s:'
                              %self.sending_msg_list[0], 'command not found')
            except ConnectionResetError and ConnectionRefusedError and OSError and IndexError as e:
                print(time.strftime("%Y-%m-%d %X", time.localtime()), '[+]client: -bash :', e,'Restart client')
                selectors_client().start()

    def put(self):
         '''
         上传函数
         :param:cmd:上传命令
         :return:
         '''
         if os.path.exists(self.file_path) and os.path.isfile(self.file_path):
             self.file_size = os.path.getsize(self.file_path)
             data_header = {"client": {
                 "action": "put",
                 "file_name": self.file_name,
                 "size": self.file_size}}
             self.client.send(json.dumps(data_header).encode())
             print(time.strftime("%Y-%m-%d %X", time.localtime()), '[+]server: -bash : %s '
                   % self.client.recv(1024).decode())
             with open(self.file_path, 'rb') as file_object:
                 for line in file_object:
                     self.client.send(line)
                 file_object.close()
             print(self.client.recv(1024).decode())
         else:
             print(time.strftime("%Y-%m-%d %X", time.localtime()),'[+]client: -bash :%s : No such file'
                   %self.file_name)

    def get(self):
        '''
        下载函数
        :param:cmd 下载命令
        :return:
        '''
        os.chdir(setting.client_download_path)
        data_header = {"client": {
            "action": "get",
            "file_name": self.file_name,
            "size": 0}}
        self.client.send(json.dumps(data_header).encode())
        self.data = self.client.recv(1024)
        if self.data.decode() == '404':
            print(time.strftime("%Y-%m-%d %X", time.localtime()),
                  '[+]server: -bash : %s : No such file' % (self.file_path))
        else:
            print(time.strftime("%Y-%m-%d %X", time.localtime()),
                  "[+]server: -bash : File ready to get File size is :", self.data.decode())
            new = random.randint(1, 100000)
            file_object = open((self.file_name + '.' + (str(new))), 'wb')
            received_size = 0
            file_size = int(self.data.decode())
            while received_size < file_size:
                if file_size - received_size > 1024:
                    size = 1024
                elif file_size < 1024:
                    size = file_size
                else:
                    size = file_size - received_size
                recv_data = self.client.recv(size)
                received_size += len(recv_data)
                file_object.write(recv_data)
            else:
                file_object.flush()
                file_object.close()
                time.sleep(0.1)
                print(time.strftime("%Y-%m-%d %X", time.localtime()),
                      "[+]client: -bash :File get done File size is :", file_size)

    def connect(self, ip, port):
        '''
        链接函数
        :param ip:
        :param port:
        :return:
        '''
        self.client.connect((ip, port))