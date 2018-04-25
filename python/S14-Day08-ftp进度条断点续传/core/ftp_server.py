#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Colin Yao
'''
ftp_server交互程序
'''
import os
import sys
import time
import json
import shelve
import hashlib
import socket
import traceback
import socketserver
BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from conf import setting
from core.commands import Commands
from src.total_size_class import quota

class Ftp_server(socketserver.BaseRequestHandler):
    '''
    ftp_server类,socketserver
    '''
    def parsecmd(self,data):
        '''
        命令传输方法
        :param data:json
        :return:
        '''
        data = json.loads(data.decode())
        file_action = data["test1"]["action"]
        file_path = data["test1"]["file_name"]
        file_size = int(data["test1"]["size"])
        file_obj = (setting.data_path+setting.file_object)
        file_md5 = hashlib.md5()
        print('from ip : %s information : %s' % (self.client_address[0], self.data.decode()))
        if setting.os_res == 'Windows':
            if os.getcwd() == (setting.bin_path):
                os.chdir(file_obj )#固定用户工作家目录
            else:
                try:
                    with open(setting.path_file, 'r')  as f:
                        f1 = []
                        f2 = f.readline().split('\\')
                        f1.append(f2)
                    f3 = os.getcwd()
                    f4 = f3.split('\\')
                    if f4[5] == f1[0][1] and f4[6] == f1[0][2]:
                        pass
                    else:
                        os.chdir(file_obj )
                except IndexError as e:
                    os.chdir(file_obj)
        elif setting.os_res == 'Linux':
            if os.getcwd() == (setting.bin_path):
                os.chdir(file_obj )
            else:
                try:
                    with open(setting.path_file, 'r')  as f:
                        f1 = []
                        f2 = f.readline().split('/')
                        f1.append(f2)
                    f3 = os.getcwd()
                    f4 = f3.split('/')
                    if f4[5] == f1[0][1] and f4[6] == f1[0][2]:
                        pass
                    else:
                        os.chdir(file_obj )
                except IndexError as e:
                    os.chdir(file_obj)

        file_obj_size = quota(file_obj).directory_size()#用户家目录文件大小file_obj_size用户磁盘配额大小 quota_size
        user_info = shelve.open(setting.data_path + setting.file_object)
        if setting.os_res == 'Windows':
            with open(setting.path_file, 'r')  as f:
                f1 = []
                f2 = f.readline().split('\\')
                f1.append(f2)
                user_name_key = f1[0][1]
                self.quota_user_size = user_info[user_name_key][3]
                user_info.close()
        elif setting.os_res == 'Linux':
            with open(setting.path_file, 'r')  as f:
                f1 = []
                f2 = f.readline().split('/')
                f1.append(f2)
                user_name_key = f1[0][1]
                self.quota_user_size = user_info[user_name_key][3]
                user_info.close()
        try:
            if file_action == 'put':#上传方法
                spare_size = (self.quota_user_size - file_obj_size)

                def file_tr():
                    '''
                    文件传输类
                    :return:
                    '''
                    md5_file = hashlib.md5()
                    self.request.send(str(file_size).encode())
                    file_object = open((file_path + '.new'), 'wb')
                    received_size = 0
                    while received_size < file_size:
                        if file_size - received_size > 1024:
                            size = 1024
                        elif file_size < 1024:
                            size = file_size
                        else:
                            size = file_size - received_size
                        recv_data = self.request.recv(size)
                        received_size += len(recv_data)
                        md5_file.update(recv_data)
                        file_object.write(recv_data)
                        #print(file_size, received_size)
                    else:
                        print('[+]File Recv Successful')
                        file_object.close()
                        self.request.send(b'File Data Recv Successful Md5:%s'%(md5_file.hexdigest().encode()))
                        os.rename((file_path + '.new'),file_path) #重命名文件
                        #self.request.send(b'File Data Recv Successful')
                def put_size():
                    '''
                    put #磁盘限额和断点续传的处理
                    :return:
                    '''
                    if file_size <= spare_size:
                        if os.path.exists(file_path + '.new'):
                            new_size = os.path.getsize(file_path + '.new')
                            if new_size == 0 or new_size>file_size:
                                file_tr()
                            else:
                                self.request.send(str(new_size).encode())
                        else:
                            file_tr()#如果不存在.new的临时文件就执行文件传输类
                    elif file_size > spare_size or spare_size == 0:
                        print('[+] Server Spare_size not enough',self.data.decode())
                        self.request.send(b'not enough Spare_size')
                if os.path.exists(file_path) == False:#文件路径不存在
                        put_size()
                else:#路径存在处理
                    if file_path == '.':
                        self.request.send(b"-b:bash:[+]Server[%s]---file is no valid." % file_path.encode())
                    else:
                        os.remove(file_path)#保持文件最新,put bug fix
                        put_size()

            elif file_action == 'resume_put':#断点续传处理
                spare_size = (self.quota_user_size - file_obj_size)
                def resume_put_file_tr():
                    md5_file = hashlib.md5()
                    self.request.send(b'read recv resume data')
                    if os.path.exists(file_path + '.new'):
                        file_object = open((file_path + '.new'), 'ab')
                        received_size = 0
                        while received_size < file_size:
                            if file_size - received_size > 1024:
                                size = 1024
                            elif file_size < 1024:
                                size = file_size
                            else:
                                size = file_size - received_size
                            recv_data = self.request.recv(size)
                            received_size += len(recv_data)
                            md5_file.update(recv_data)
                            file_object.write(recv_data)
                            #print(file_size, received_size)
                        else:
                            file_object.close()
                            print('[+]File Resume Recv Successful',time.time())
                            os.rename((file_path + '.new'), (file_path))
                            self.request.sendall(b'File Resume Recv Successful Md5 %s'%(md5_file.hexdigest().encode()))
                def resume_put_size():
                    '''
                     断点续传方法,判断磁盘限额
                    :return:
                    '''
                    if file_size <= spare_size:
                        resume_put_file_tr()
                    elif file_size > spare_size or spare_size == 0:
                        print('[+] Server Spare_size not enough', self.data.decode())
                        self.request.send(b'not enough Spare_size')
                if os.path.exists(file_path) == False:#文件路径不存在处理
                    resume_put_size()
                else:#保持文件最新
                    os.remove(file_path)
                    resume_put_size()

            elif file_action == 'get':#下载方法
                os.chdir(setting.ftp_path) #公共下载目录为db/Upload,客户端默认下载路径为用户家目录
                if os.path.isfile(file_path) and os.path.exists(file_path):
                    if setting.os_res == 'Windows':
                        file_size = os.path.getsize(setting.ftp_path + '\\' + file_path)
                        file_obj_path = (setting.ftp_path + '\\' + file_path)
                    elif setting.os_res == 'Linux':
                        file_size = os.path.getsize(setting.ftp_path + '/' + file_path)
                        file_obj_path = (setting.ftp_path + '/' + file_path)
                    file_obj = open(file_path, "rb") #磁盘配额-用户家文件总大小=剩余磁盘空间,用剩余磁盘空间与下载文件大小做对比
                    spare_size = (self.quota_user_size - file_obj_size)
                    if file_size <= spare_size:
                        self.request.send(str(file_size).encode())
                        self.request.recv(1024)
                        for line in file_obj:#md5校验
                            file_md5.update(line)
                            self.request.send(line)
                        file_obj.close()
                        self.request.send(b"[+]File[%s]Send Done File_Md5:%s" %(file_path.encode(),file_md5.hexdigest().encode()))
                    elif file_size > spare_size or spare_size ==0 :#磁盘配额处理,文件总大小>剩余空间发送消息给客户端
                        self.request.send(str(0).encode())
                        self.request.recv(1024)
                        self.request.send(b'-b:bash: There is Not Enough Space The rest is %smb'
                                          %str(round(spare_size / 1024 / 1024)).encode())
                else:
                    if file_path == '.':#get不存在文件,导致json.decoder.JSONDecodeError,处理方式传一个json
                        self.request.send(b"-b:bash:[+]Server[%s]---file is no valid."%file_path.encode())
                    else:
                        self.request.send(str(0).encode())
                        self.request.recv(1024)
                        self.request.send(b"-b:bash:[+]Server[%s]---file is no valid."%file_path.encode())

            elif file_action == 'pls':#查看FTP文件方法
               os.chdir(setting.ftp_path)
               res = Commands(file_path).ls()
               if setting.os_res == 'Windows':
                   res1 = res.decode('gbk')
               elif setting.os_res == 'Linux':
                   res1 = res.decode()
               if len(res1) == 0:#粘包处理
                   pass
               self.request.send(str(len(res1.encode())).encode('utf-8'))
               client_send = self.request.recv(1024)
               self.request.send(res1.encode('utf-8'))
               self.request.send(b'-bash: [%s] [%s]:' %(file_action.encode(),file_path.encode()))
               os.chdir(file_obj)

            elif file_action == 'ls':#查看文件方法
                res = Commands(file_path).ls()#上一版本没有文件大小信息,只是传送了列表
                if setting.os_res == 'Windows':
                    res1 = res.decode('gbk')
                elif setting.os_res == 'Linux':
                    res1 = res.decode()
                if len(res1) == 0:#粘包处理
                    pass
                self.request.send(str(len(res1.encode())).encode('utf-8'))
                client_send = self.request.recv(1024)
                self.request.send(res1.encode('utf-8'))
                self.request.send(b'-bash: [%s] [%s]:'% (file_action.encode(),file_path.encode()))

            elif  file_action== 'cd':#cd目录
                if os.path.exists(file_obj + '\\' + file_path) == True:
                    os.chdir(file_obj + '\\'+ file_path)
                    self.request.send(b'-bash: [%s] [%s]:'%(file_action.encode(),file_path.encode()))
                else:
                    self.request.send(b'-bash:Directory Exitis')

            elif file_action == 'mkdir':#创建目录
                if os.path.exists(file_path) == True:
                    self.request.send(b'-bash: directory exitis ')
                else:
                    res = Commands(file_path).mkdir()
                    self.request.send(b'-bash: [%s] [%s]:'%(file_action.encode(),file_path.encode()))

            elif file_action == 'rm':#文件删除
                if os.path.isfile(file_path) == True:
                    res = Commands(file_path).rm()
                    self.request.send(b'-bash: [%s] [%s]:'%(file_action.encode(),file_path.encode()))
                else:
                    self.request.send(b'-bash: [%s]: Not file'%file_path.encode())

            elif file_action == 'drm':#目录删除
                if os.path.isdir(file_path) == True:
                    Commands(file_path).drm()
                    self.request.send(b'-bash: %s: Delete OK'%file_path.encode())
                else:
                    self.request.send(b'-bash: [%s]: No such File or Directory '%file_path.encode())

            elif file_action == 'e1930b4927e6b6d92d120c7c1bba3421':#文件配额处理
                spare_size = (self.quota_user_size - file_obj_size)
                self.request.send(b'-bash: [+] Not Enough Space Spare_size is %smb'%str(round(spare_size/1024/1024)).encode())
            else:
                self.request.send(b'-bash:Command or File Not Found ')
        except Exception and UnicodeDecodeError:
            traceback.print_exc()

    def handle(self):
        '''
        handle socketserver写法
        :return:
        '''
        print("[+] Server is running on port:62000", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        while True:
            try:
                #调整一下socket.socket()的位置每次重新连接都生成新的socket实例,避免因为意外而导致socket断开连接
                print("[+] Connect success -> %s at ", self.client_address, time.strftime("%Y%m%d %H:%M:%S", time.localtime()))
                self.request.send(b'\033[34;1mWelcome,-bash version 0.0.1-release \033[0m ')
                while True:
                    self.data = self.request.recv(1024)
                    data = self.data
                    self.parsecmd(data)
                    if not self.data:
                        print("[+]Error: Client is lost")
                        break
            except socket.error :
                print("[+]Error get connect error")
                break
            continue