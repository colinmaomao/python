#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Colin Yao

import os
import sys
import pickle, json
import platform
import threading
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
from conf import setting
from model import paramiko


class server_ftp(object):
    '''
    serverftp类
    '''
    def __init__(self, group_input,server_input,fileobject,filename):
        '''
        构造函数
        :param group_input:
        :param server_input:
        :param fileobject:
        '''
        self.group_input = group_input
        self.server_input = server_input
        self.fileobject = fileobject
        self.filename = filename

        with open(setting.server_list_path, 'rb') as dict_file_object:
            self.server_list_dict = pickle.load(dict_file_object)  # server_list_dict服务器字典变量
            dict_file_object.close()
        if self.group_input in self.server_list_dict['machine']:
            if self.server_input in self.server_list_dict['machine'][self.group_input]:
                self.server_ip = self.server_list_dict['machine'][self.group_input][self.server_input]['ip']
                self.server_port = int(self.server_list_dict['machine'][self.group_input][self.server_input]['port'])
                self.server_username = self.server_list_dict['machine'][self.group_input][self.server_input]['username']
                self.server_passwd = self.server_list_dict['machine'][self.group_input][self.server_input]['passwd']
                self.transport = paramiko.Transport((self.server_ip, self.server_port))
                self.transport.connect(username=self.server_username, password=self.server_passwd)
                self.sftp = paramiko.SFTPClient.from_transport(self.transport)
            else:
                pass
        else:
            print('not allow')
    def upload(self):
        '''
        上传函数
        :param command:
        :return:
        '''
        try:
            os.chdir(setting.upload_path)
            self.sftp.put(self.filename,self.fileobject)
        except FileNotFoundError as e:
            print('system error ', e)

    def download(self):
        '''
        下载函数
        :param
        :return:
        '''
        os.chdir(setting.download_path)
        try:
            if platform.system() == 'Windows':
                self.sftp.get(self.fileobject, (setting.download_path + '\\' + self.filename))
            else:
                self.sftp.get(self.fileobject, (setting.download_path + '/' + self.filename))
            if os.path.exists(setting.download_path + '\\' + self.filename):
                print('file download complete')
            else:
                print('file download error')
        except FileNotFoundError as e:
            print('system error ', e)
            os.remove(self.filename)