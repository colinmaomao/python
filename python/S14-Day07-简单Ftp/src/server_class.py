#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Colin Yao
'''ftpserver类'''
import os,socket
class Server_class(object):
    def __init__(self,ip_addr,port):
        self.ip_addr = ip_addr
        self.port = port
        self.server = socket.socket()