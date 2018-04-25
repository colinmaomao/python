#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Colin Yao
import logging
import os,sys,platform,json
BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR) #添加环境变量
os_res = platform.system()
if  os_res == 'Windows':
    data_path = os.path.join(BASE_DIR + '\db')
    ftp_path = os.path.join(BASE_DIR + '\db\pub')
    path_file = os.path.join(BASE_DIR + '\db\\user_path\path')

else:
    data_path = os.path.join(BASE_DIR + '/db')
    ftp_path = os.path.join(BASE_DIR + '\db\pub')
    path_file = os.path.join(BASE_DIR + '/db/user_path/path')

with open(path_file, 'r', encoding='utf-8')as f:
    file = f.readlines()
    file_object=file[0]