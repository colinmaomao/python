#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Colin Yao
import os,sys,time
import subprocess,subprocess,json
import socketserver,socket,traceback

BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from core.main import Admin
from core.auth import Auth_ftp
from core.commands import Commands
from conf import setting
from src.server_class  import Server_class


class Ftp_server(socketserver.BaseRequestHandler):
    #都懵比了很多代码重复了、等着重新回炉下~~~
    def parsecmd(self,data):

        data = json.loads(data.decode())
        file_action = data['test1']['action']
        file_path = data['test1']['file_name']
        file_size = int(data['test1']['size'])
        file_obj = setting.file_object
        print('from ip : %s information : %s' % (self.client_address[0], self.data.decode()))

        try:
            if file_action == 'put':
                os.chdir(file_obj)  # 默认用用户的目录作为上传目录
                def file_tr():
                    self.request.send(b'recv data')
                    file_object = open(file_path, 'wb')
                    received_size = 0
                    while received_size < file_size:
                        recv_data = self.request.recv(1024)
                        file_object.write(recv_data)
                        received_size += len(recv_data)  # 规定多少但不一定收到那么多
                        print(file_size, received_size)
                    else:
                        print('[+]File Recv Successful')
                        file_object.close()

                if os.path.exists(file_path) == False:  # 判断文件是否存在
                    file_tr()
                else:
                    self.request.send(b'[+] this file[%s] will cover ....' % file_path.encode())
                    file_tr()

            elif file_action == 'get':
                os.chdir(setting.ftp_path)  # get对象工作的目录pub
                # # get文件首先需要其他目录,或者更改名字 ,然后进行getget的地址应该是自己家目录的地址
                # # 下载文件时候客户端在用户目录下面去下载
                #判断size不同os的路径不同
                if setting.os_res == 'Windows':
                    file_size = os.path.getsize(setting.ftp_path+'\\'+file_path)
                if setting.os_res == 'Linux':
                    file_size = os.path.getsize(setting.ftp_path + '/' + file_path)
                try:
                    if os.path.exists(file_path) == True:  # 判断文件路径# 是否存在
                        if os.path.isfile(file_path):
                            file_obj = open(file_path, "rb")
                            #直接copy 客户端put的代码就可以,这里self.conn.send 改为request.send
                            self.request.send(str(file_size).encode())
                            self.request.recv(1024)
                            for line in file_obj:
                                self.request.send(line)
                            file_obj.close()
                            self.request.send(b"-b:bash:[+]Server[%s]---send file down-----"%file_path.encode())
                        else:
                            print('[+]file is no valid.')
                            self.request.send(b"-b:bash:[+]Server[%s]---file is no valid.-----" % file_path.encode())
                            #这里不写上下俩条的话客户端就会卡住、处于一直等待中
                    else:
                        self.request.send(b"-b:bash:[+]Server[%s]---file is no valid.-----" % file_path.encode())
                 # except json.decoder.JSONDecodeError:
                 #     self.request.send(b'-b:bash:[+]what are you doing???')
                except:
                    pass

            elif  file_action== 'cd':
                if os.path.exists(file_path) == True:
                    res = Commands(file_path).cd()
                    self.request.send(b'-bash: [%s] [%s]: ' % (file_action.encode(), file_path.encode()))
                else:
                    self.request.send(b'-bash:Directory Exitis')

            elif file_action == 'mkdir':
                    os.chdir(file_obj)
                    # 文件夹mkdir命令处理,如果是windows默认应该是gbk生成的bytes类型'''
                    if os.path.exists(file_path) == True:# 进入要传递目录
                        self.request.send(b'-bash: directory exitis ')
                    else:
                        res = Commands(file_path).mkdir()
                        self.request.send(b'-bash: [%s] [%s]:' % (file_action.encode(), file_path.encode()))

            elif file_action == 'ls':  #测试利用json返回命令结果、反正挺好玩的!!!!用subporcess 用的挺high的
                res = os.listdir()
                res = json.dumps(res)
                self.request.send(res.encode())
                # '''文件删除命令处理, 如果是windows默认应该是gbk生成的bytes类型'''

            elif file_action == 'rm':
                os.chdir(file_obj)
                if os.path.isfile(file_path) == True:
                    res = Commands(file_path).rm()
                    self.request.send(b'-bash: [%s] [%s]:' % (file_action.encode(), file_path.encode()))
                else:
                    self.request.send(b'-bash: [%s]: Not file  ' % file_path.encode())
                    # 目录删除命令处理, 如果是windows默认应该是gbk生成的bytes类型'''

            elif file_action == 'drm':
                os.chdir(file_obj)  # 进入要传递目录
                if os.path.isdir(file_path) == True:  # 判断是否是目录
                    Commands(file_path).drm()
                    self.request.send(b'-bash: %s: Delete OK '%file_path.encode())
                else:
                    self.request.send(b'-bash: [%s]: No such File or Directory ' %file_path.encode())
            else:
                self.request.send(b'-bash:Command or File Not Found ')

        except Exception and UnicodeDecodeError:
            traceback.print_exc()


    def handle(self):
        print("[+] Server is running on port:62000", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        while True:
            try:  # 调整一下socket.socket()的位置每次重新连接都生成新的socket实例,避免因为意外而导致socket断开连接
                print("[+] Connect success -> %s at ", self.client_address, time.strftime("%Y%m%d %H:%M:%S", time.localtime()))
                self.request.send(b'\033[34;1mWelcome,-bash version 0.0.1-release \033[0m ')
                while True:
                    self.data = self.request.recv(1024)
                    data = self.data
                    self.parsecmd(data)
                    if not self.data:
                        print("[+]Error: Client is lost")
                        break
            except socket.error:
                print("[+]Error get connect error")
                break
            continue

#socketserver.ThreadingTCPServer(('127.0.0.1', 62000), Ftp_server).serve_forever()