#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Colin Yao
import os, sys
import platform, socket
import time,hashlib,json
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)  # 添加环境变量
from conf import setting
from core.commands import Commands
from conf import setting

# from src.server_class  import Server_class
'''定义client连接的协议和方式后面需要补充'''
'''创建连接输入IP地址和密码'''


class Ftp_client(object):

    def link(self):
     try:
        os.chdir(setting.file_object) #直接进入FTP指定的用户目录
        self.sending_msg_list = []
        self.ip_addr = '127.0.0.1'
        self.ip_port = 62000
        self.client = socket.socket()
        self.client.connect((self.ip_addr, self.ip_port))
        while True:
            self.sending_msg = None
            self.data = self.client.recv(1024)
            print("[+]Server>>>recv: %s" % self.data.decode())
            self.menu()
            sending_msg = input('请输入命令>>>:')
            self.sending_msg_list = sending_msg.split()
            if len(sending_msg)  == 0:
                data_header = {
                    'test1': {
                        'action': '',
                        'file_name': '',
                        'size': 0
                    }
                }
                self.client.send(json.dumps(data_header).encode())
            elif len(sending_msg) >= 2 :
                if setting.os_res == 'Windows':
                    try :
                        new_path = self.sending_msg_list[1].encode('utf-8')
                        self.res_new = self.sending_msg_list[1].strip().split('\\')  # 截取获得文件名
                        self.file_name1 = self.res_new[-1]

                    except IndexError:
                        pass
                elif setting.os_res == 'Linux':
                    try:
                        self.res_new = self.sending_msg_list[1].strip().split('/')
                        self.file_name1 = self.res_new[-1]
                    except IndexError:
                        pass
                if self.sending_msg_list[0] == "put":
                    try:
                        self.put(self.sending_msg_list[1])
                    except IndexError:
                        self.client.send('put'.encode())

                if self.sending_msg_list[0] == "get":
                    try:
                        self.get(self.file_name1)
                    except IndexError and ValueError:
                        self.client.send('get'.encode())

                elif self.sending_msg_list[0] == "exit":
                    break
                else:#cd ls rm drm mkdir 命令等
                    try:
                        data_header = {
                            'test1': {
                                'action': self.sending_msg_list[0],
                                'file_name': self.file_name1,
                                'size': 0
                            }
                        }
                        self.client.send(json.dumps(data_header).encode())
                    except AttributeError:
                        data_header = {
                            'test1': {
                                'action': self.sending_msg_list[0],
                                'file_name': '',
                                'size': 0
                            }
                        }
                        self.client.send(json.dumps(data_header).encode())
     except ConnectionResetError and ConnectionAbortedError:
         print("[+]Server is Down ....Try to Reconnect......")
         self.link()

    def get(self,file_name):
        data_header = {
            'test1': {
                'action': 'get',
                'file_name': file_name,
                'size': 0
            }
        }
        #这里没做同名文件判断,下一次补充
        self.client.send(json.dumps(data_header).encode())  #发送get请求
        print(os.getcwd())
        self.data = self.client.recv(1024)     #拿到size
        self.client.send(b'come on')
        file_size = int(self.data.decode())
        def file_tr():
            file_object = open(file_name, 'wb')
            received_size = 0
            while received_size < file_size:
                recv_data = self.client.recv(1024)
                file_object.write(recv_data)
                received_size += len(recv_data)  # 规定多少但不一定收到那么多
                print(file_size, received_size)
            else:
                print('[+]Client:File Recv Successful')
                file_object.close()
        if os.path.exists(file_name) == False:  # 判断本地目录文件是否存在
            file_tr()
        else:
            print('文件已经存在将要覆盖')
            file_tr()

    def put(self,file_name):
        if os.path.exists(file_name)== True: #判断文件路径# 是否存不存在
            if os.path.isfile(file_name):
                file_obj = open(file_name, "rb")
                data_header = {
                    'test1': {
                        'action': 'put',
                        'file_name': self.file_name1,
                        'size': os.path.getsize(self.sending_msg_list[1].encode())
                    }
                }
                self.client.send(json.dumps(data_header).encode())
                for line in file_obj:
                   self.client.send(line)
                file_obj.close()
                print("[+]-----send file down-----")
            else:
                print('[+]file is no valid.')
                self.client.send('cmd'.encode())
        else:
            print('[+] File Not Found')
            data_header = {
                'test1': {
                    'action': 'aaaa',
                    'file_name': '',
                    'size': 0
                }
            }
            self.client.send(json.dumps(data_header).encode())

    def menu(self):
        menu = '''
        ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
            帮    助     请注意windows和linux的路径稍有不同    
            查看文件     ls(file)    eg: ls /tmp/Python3.6.3/README
            进入目录     cd          eg: cd /tmp/python
            创建目录     mkdir(dir)  eg: mkdir  /tmp/python
            删除文件     rm          eg: rm  /tmp/python/README 
            删除目录     drm         eg: drm /tmp/python
            上   传      put         eg: put  /tmp/python/README 
            下   载      get         eg: get /tmp/python/README
            登   出      exit
            默认上传文件夹         用户目录下用用户名的命名的文件夹
            默认下载文件夹         db/Upload
         ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
            '''
        print(menu)