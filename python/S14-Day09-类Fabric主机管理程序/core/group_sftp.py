#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Colin Yao
import os
import sys
import pickle
import platform
import threading
import time,random
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
from conf import setting
from model import paramiko

class group_ftp(object):
    '''
    serverftp类
    '''
    def __init__(self,group_input,fileobject,filename):
        '''
        构造函数
        :param group_input:
        :param server_input:
        :param fileobject:
        '''
        self.group_input = group_input
        self.fileobject = fileobject
        self.filename = filename

        with open(setting.server_list_path, 'rb') as dict_file_object:
            self.server_list_dict = pickle.load(dict_file_object)  # server_list_dict服务器字典变量
            dict_file_object.close()

    def upload(self):
        '''
        上传函数
        :param command:
        :return:
        '''
        try:
            os.chdir(setting.upload_path)
            for s in self.server_list_dict['machine'][self.group_input]:
                self.server_ip = self.server_list_dict['machine'][self.group_input][s]['ip']
                self.server_port = int(self.server_list_dict['machine'][self.group_input][s]['port'])
                self.server_username = self.server_list_dict['machine'][self.group_input][s]['username']
                self.server_passwd = self.server_list_dict['machine'][self.group_input][s]['passwd']
                self.transport = paramiko.Transport((self.server_ip, self.server_port))
                self.transport.connect(username=self.server_username, password=self.server_passwd)
                self.sftp = paramiko.SFTPClient.from_transport(self.transport)
                t = threading.Thread(target=self.sftp.put, args=(self.filename, self.fileobject))
                t.start()
        except FileNotFoundError as e:
            print('system error ', e)

    def download(self):
        '''
        下载函数
        :param
        :return:
        '''
        os.chdir(setting.download_path)
        for s in self.server_list_dict['machine'][self.group_input]:
            self.server_ip = self.server_list_dict['machine'][self.group_input][s]['ip']
            self.server_port = int(self.server_list_dict['machine'][self.group_input][s]['port'])
            self.server_username = self.server_list_dict['machine'][self.group_input][s]['username']
            self.server_passwd = self.server_list_dict['machine'][self.group_input][s]['passwd']
            self.transport = paramiko.Transport((self.server_ip, self.server_port))
            self.transport.connect(username=self.server_username, password=self.server_passwd)
            self.sftp = paramiko.SFTPClient.from_transport(self.transport)
            try:
                if platform.system() == 'Windows':
                    #self.sftp.get(self.fileobject, (setting.download_path + '\\' + self.filename))
                    t = threading.Thread(target=self.sftp.get,args=(self.fileobject, (setting.download_path + '\\' + self.filename)))
                    t.start()
                    #time.sleep(10)
                else:
                    #self.sftp.get(self.fileobject, (setting.download_path + '/' + self.filename))
                    t = threading.Thread(target=self.sftp.get,
                                         args=(self.fileobject, (setting.download_path + '\\' + self.filename)))
                    t.start()
                if os.path.exists(setting.download_path + '\\' + self.filename):
                    print('file download complete')
                else:
                    print('file download error')
            except FileNotFoundError as e:
                print('system error ', e)
                os.remove(self.filename)