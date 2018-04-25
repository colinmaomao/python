#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Colin Yao
import os,sys
BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR) #添加环境变量
from core import ftp_server

if __name__ == '__main__':
    ftp_server.socketserver.ThreadingTCPServer(('127.0.0.1', 62000), ftp_server.Ftp_server).serve_forever()