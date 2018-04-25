#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Colin Yao
'''ftpclient程序'''
import os
import sys
BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from  core import client_main

if __name__ == '__main__':
    f = client_main.client_ftp()
    f.start()
