#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Colin Yao
'''ftpserver程序'''
import os
import sys
BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from core import  server_main

if __name__ == '__main__':
    f = server_main.server_ftp()
    f.start()