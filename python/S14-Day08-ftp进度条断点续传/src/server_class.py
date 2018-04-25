#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Colin Yao
'''ftpserver基础类'''
import socket

class Server_class(object):
    '''
    server类
    '''
    def __init__(self,ip_addr,port):
        '''
        构造函数
        :param ip_addr: IP地址
        :param port: 端口
        '''
        self.ip_addr = ip_addr
        self.port = port
        self.server = socket.socket()