#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Colin Yao

import os
import json
import sys
import random
import time
import select
import socket
import queue

BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from conf import setting

class select_ftp(object):
    """Ftp server"""
    def __init__(self, ip, port):
        '''
        构造函数
        :param ip: 监听IP
        :param port: 监听端口
        :return:
        '''
        self.server = socket.socket()
        self.host = ip
        self.port = port
        self.msg_dic = {}
        self.inputs = [self.server,]
        self.outputs = []
        self.file_flag = {}
        self.file_up_flag = {}


    def start(self):
        '''
        主启动函数
        :return:
        '''
        self.server.bind((self.host,self.port))
        self.server.listen(1000)
        self.server.setblocking(False)
        while True:
            readable, writeable, exceptional = select.select(self.inputs, self.outputs, self.inputs)  # 定义检测
            for r in readable:
                self.readable(r)
            for w in writeable:
                self.writeable(w)
            for e in exceptional:
                self.clean(e)


    def readable(self, ser):
        '''
        处理活动的从客户端传来的数据连接
        :param ser: socket server自己
        :return:
        '''
        if ser is self.server:
            conn, addr = self.server.accept()
            print(time.strftime("%Y-%m-%d %X", time.localtime()), ': echoing: newlink ',addr)
            self.inputs.append(conn)
            self.msg_dic[conn] = queue.Queue()
        else:
            try :
                data = ser.recv(1024)
                cmd = data.decode()
                cmd_str = cmd.split()[0]
                if len(cmd.split()) == 2 and hasattr(self, cmd_str):
                    print(time.strftime("%Y-%m-%d %X", time.localtime()), ': echoing: newlink ', cmd)
                    filename = cmd.split()[1]
                    func = getattr(self, cmd_str)
                    func(ser, filename)
                else:
                    self.upload(ser, data)
            except ConnectionResetError as e:
                print(time.strftime("%Y-%m-%d %X", time.localtime()), ": client lost",ser)
                self.clean(ser)
            except UnicodeDecodeError as e :
                self.upload(ser, data)


    def writeable(self, conn):
        '''
        处理活动的传回客户端的数据连接
        :param conn: 客户端连接
        :return:
        '''
        try :
            data_to_client = self.msg_dic[conn].get()
            conn.send(data_to_client)
        except Exception as e :
            print(time.strftime("%Y-%m-%d %X", time.localtime()), ': error client lost')
            self.clean(conn)
            del self.file_flag[conn]
        else:
            self.outputs.remove(conn)
            filename = self.file_flag[conn][2]
            size = self.file_flag[conn][0]
            trans_size = self.file_flag[conn][1]
            if trans_size < size :
                self.load(conn, filename, size)
            else:
                del self.file_flag[conn]


    def clean(self, conn):
        '''
        连接完成，收尾处理
        :param conn: 客户端连接
        :return:
        '''
        if conn in self.outputs:
            self.outputs.remove(conn)
        if conn in self.inputs:
            self.inputs.remove(conn)
        if conn in self.msg_dic:
            del self.msg_dic[conn]


    def put(self, conn, filename):
        '''
        客户端上传函数
        :param conn:
        :param filename:
        :return:
        '''
        os.chdir(setting.upload_path)
        if filename == "done(status:200)":
            del self.file_up_flag[conn]
        else :
            if os.path.isfile(filename):
                try:
                   new = random.randint(1, 100000)
                   self.rename(filename, (filename + '.' + str(new)))
                except FileExistsError:
                    os.remove(filename)

            print(time.strftime("%Y-%m-%d %X", time.localtime()), ': server recv download data')
            conn.send(b'200')
            self.file_up_flag[conn] = filename


    def upload(self, conn, data):
        '''
        客户端上传，数据接收函数
        :param conn: 客户端连接
        :param data: 客户端上传数据
        :return:
        '''
        os.chdir(setting.upload_path)
        if conn in self.file_up_flag:
            filename = self.file_up_flag[conn]
            with open(filename, 'ab') as file_object:
                file_object.write(data)



    def get(self, conn, filename):
        '''
        客户端下载函数
        :param conn:
        :param filename:
        :return:
        '''
        os.chdir(setting.download_path)
        msg_dic = {  # 下载文件信息
            "action" : "get",
            "filename" : filename,
            "size" : None,
            "status" : 550
        }
        if os.path.isfile(filename):
            size = os.stat(filename).st_size
            msg_dic['size'] = size
            msg_dic['status'] = 200
        conn.send(json.dumps(msg_dic).encode())
        if msg_dic['status'] == 200:
            self.load(conn, filename, size)


    def load(self, conn, filename, size):
        '''
        客户端下载，数据传输函数
        :param conn:
        :param filename:
        :param size:
        :return:
        '''
        if conn in self.file_flag:
            trans_size = self.file_flag[conn][1]
        else:
            trans_size = 0
        with open(filename, "rb") as f:
            f.seek(trans_size)
            data = f.readline()
            self.msg_dic[conn].put(data)
            self.outputs.append(conn)
            trans_size += len(data)
            self.file_flag[conn] = [size, trans_size, filename]

    def rename(self, old_name, new_name):
        '''
        重命名函数
        :param old_name:
        :param new_name:
        :return:
        '''
        if os.path.exists(new_name):
            os.remove(new_name)
        os.rename(old_name, new_name)