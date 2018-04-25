#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Colin Yao
'''ftp客户端交互程序'''
import os
import sys
import socket
import time
import hashlib
import json
import progressbar
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from conf import setting

class Ftp_client(object):
    '''
    Ftp_client 类
    '''
    def link(self):
        '''
        link:链接函数
        :return:
        '''
        try:
            self.sending_msg_list = []
            self.ip_addr = '127.0.0.1'
            self.ip_port = 62000
            self.client = socket.socket()
            self.client.connect((self.ip_addr, self.ip_port))
            while True:
                self.sending_msg = None
                self.data = self.client.recv(1024)
                print("\033[34;1m[+]Server>>>recv: %s\033[0m" % self.data.decode())
                self.menu()
                sending_msg = input('请输入命令>>>:')
                self.sending_msg_list = sending_msg.split()

                if len(self.sending_msg_list) == 0:  # 无键盘输出与服务器交互
                    data_header = {"test1": {"action": "", "file_name": "", "size": 0}}
                    self.client.send(json.dumps(data_header).encode())
                elif len(self.sending_msg_list) == 1:
                    if self.sending_msg_list[0] == 'ls' or self.sending_msg_list[0] == 'pls':
                        self.cmd()
                    else:  # get bug_fix
                        data_header = {"test1": {"action": self.sending_msg_list[0], "file_name": ".", "size": 0}}
                        self.client.send(json.dumps(data_header).encode())
                elif len(self.sending_msg_list) >= 2:  # windows/linux文件路径处理
                    try:
                        if setting.os_res == 'Windows':
                            new_path = self.sending_msg_list[1].encode('utf-8')
                            self.res_new = self.sending_msg_list[1].strip().split('\\')
                            self.file_name1 = self.res_new[-1]
                        elif setting.os_res == 'Linux':
                            self.res_new = self.sending_msg_list[1].strip().split('/')
                            self.file_name1 = self.res_new[-1]
                    except IndexError:
                        pass
                    if self.sending_msg_list[0] == "put":  # 命令处理
                        try:
                            self.put(self.sending_msg_list[1])
                        except IndexError:
                            self.client.send('put'.encode())
                    elif self.sending_msg_list[0] == "get":
                        try:
                            self.get(self.file_name1)
                        except IndexError and ValueError:
                            self.client.send('get'.encode())

                    elif self.sending_msg_list[0] == "exit":
                        break
                    elif self.sending_msg_list[0] == "ls" or self.sending_msg_list[0] == "pls":
                        try:
                            self.cmd()
                        except AttributeError:
                            self.cmd()
                    else:  # cd rm drm mkdir 命令等
                        try:
                            data_header = {"test1": {
                                "action": self.sending_msg_list[0],
                                "file_name": self.file_name1,
                                "size": 0}}
                            self.client.send(json.dumps(data_header).encode())
                        except AttributeError:
                            data_header = {"test1": {
                                "action": self.sending_msg_list[0],
                                "file_name": "",
                                "size": 0}}
                            self.client.send(json.dumps(data_header).encode())

        except ConnectionResetError and ConnectionAbortedError:
            print("[+]Server is Down ....Try to Reconnect......")
            self.link()

    def cmd(self):
        '''
        命令类
        :return:
        '''
        if len(self.sending_msg_list) == 1:
            data_header = {"test1": {"action": self.sending_msg_list[0], "file_name": "", "size": 0}}
        elif len(self.sending_msg_list) >= 2:
            data_header = {"test1": {"action": self.sending_msg_list[0], "file_name": self.file_name1, "size": 0}}
        self.client.send(json.dumps(data_header).encode())  # 发送cmd请求主要是ls会有粘包的可能
        cmd_res_size = self.client.recv(1024)
        self.client.send('粘包处理'.encode('utf-8'))
        cmd_res_size1 = int(cmd_res_size.decode())
        received_size = 0
        received_data = b''
        while received_size < int(cmd_res_size.decode()):
            data = self.client.recv(1024)
            received_size += len(data)
            received_data += data
        else:
            print(received_data.decode())

    def get(self, file_name):
        '''
        下载类
        :param file_name:
        :return:
        '''
        md5_file = hashlib.md5()
        data_header = {"test1": {"action": "get", "file_name": file_name, "size": 0}}
        self.client.send(json.dumps(data_header).encode())  # 发送get请求
        self.data = self.client.recv(1024)  # get_size
        if self.data.decode() == '0':
            self.client.send(b'come on')
        else:
            self.client.send(b'come on')
            file_size = int(self.data.decode())
            def file_tr():
                '''
                file_tr 文件传输类
                :return:
                '''
                P = progressbar.ProgressBar()
                N = int(self.data.decode())
                P.start(N)
                file_object = open(file_name, 'wb')
                received_size = 0
                while received_size < file_size:  # 粘包处理

                    if file_size - received_size > 1024:
                        size = 1024
                    elif file_size < 1024:  # 小于1024处理,测试发现<1024会粘包
                        size = file_size
                    else:
                        size = file_size - received_size
                    recv_data = self.client.recv(size)  # 接收数据的时候和进度条保持一致
                    received_size += len(recv_data)
                    md5_file.update(recv_data)
                    P.update(received_size)
                    file_object.write(recv_data)
                else:  # 代表文件处理完成
                    P.finish()
                    new_file_md5 = md5_file.hexdigest()
                    file_object.close()
                    time.sleep(0.1)
                    print('[+]Client:New_File[%s]Recv Done File_Md5:%s' % (file_name, new_file_md5))
            if os.path.exists(file_name) == False:
                file_tr()
            else:
                user_choice = input('文件已经存在即将要删除并下载 [y/删掉旧文件 | n/覆盖旧文件] >>>:')
                if user_choice == 'y': #文件删除操作
                    os.remove(file_name)
                    file_tr()
                elif user_choice == 'n':
                    file_tr()
                else:
                    file_tr()

    def put(self, file_name):
        '''
        上传类
        :param file_name:
        :return:
        '''
        if os.path.exists(file_name) == True:
            if os.path.isfile(file_name):
                file_obj = open(file_name, "rb")
                data_header = {"test1": {
                    "action": "put",
                    "file_name": self.file_name1,
                    "size": os.path.getsize(self.sending_msg_list[1].encode())}}
                self.client.send(json.dumps(data_header).encode())
                self.data = self.client.recv(1024)  # 有not enough 数据,还有数字字符的数据
                resume_message = (self.data.decode())
                if resume_message == 'not enough Spare_size':
                    print('[+]----Server Space not enough put smaller----')
                    data_header = {"test1": {
                        "action": "e1930b4927e6b6d92d120c7c1bba3421",
                        "file_name": "",
                        "size": 0}}
                    self.client.send(json.dumps(data_header).encode())
                else:
                    resume_size = int(self.data.decode())
                    file_send_size = os.path.getsize(self.sending_msg_list[1])
                    if resume_size < file_send_size and resume_size != 0:  # 断点续传处理
                        file_obj = open(file_name, "rb")
                        md5_file = hashlib.md5()
                        file_obj.seek(resume_size)  # seek到断点位置
                        file_resume_send_size = (os.path.getsize(self.sending_msg_list[1]) - resume_size)  # 断点大小
                        data_header = {"test1": {"action": "resume_put","file_name": self.file_name1,"size": file_resume_send_size}}
                        self.client.send(json.dumps(data_header).encode())
                        self.data = self.client.recv(1024) # 测试发送
                        P = progressbar.ProgressBar()
                        P.start(file_send_size)
                        new_size = resume_size
                        for line in file_obj:
                            self.client.send(line)
                            new_size += len(line)
                            # time.sleep(4) #查看断点续传效果
                            P.update(new_size)
                            md5_file.update(line)
                        P.finish()
                        file_obj.close()
                        print("[+]Client>>>recv:Send Resume File Done Md5", md5_file.hexdigest())
                    else:  # 文件下载处理
                        file_obj = open(file_name, "rb")
                        md5_file = hashlib.md5()
                        new_size = 0
                        P = progressbar.ProgressBar()
                        P.start(file_send_size)
                        for line in file_obj:
                            self.client.send(line)
                            new_size += len(line)
                            P.update(new_size)
                            md5_file.update(line)
                        P.finish()
                        file_obj.close()
                        print("[+]Client>>>recv:Send File Done Md5:", md5_file.hexdigest())
            else:
                print('[+]file is no valid.')
                self.client.send('cmd'.encode())
        else:
            print('[+] File Not Found')
            data_header = {"test1": {
                "action": "aaaa",
                "file_name": "",
                "size": 0}}
            self.client.send(json.dumps(data_header).encode())

    def menu(self):
        '''
        打印menu类
        :return:
        '''
        menu = '''
 ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
   进入目录     cd       eg: cd /tmp/python
   查看文件     ls       eg: ls /tmp/README
   创建目录     mkdir    eg: mkdir /tmp/python
   删除文件     rm       eg: rm /tmp/README
   删除目录     drm      eg: drm /tmp/python
   上传文件     put      eg: put /python/README
   下载文件     get      eg: get /python/README
   新增命令     pls      eg: pls 查看db/pub目录文件
   注销用户     exit
   注意事项     notice   windows和linux的路径不同
 ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
            '''
        print(menu)