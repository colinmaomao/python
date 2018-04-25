#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Colin Yao
'''主配置文件'''
import os
import sys
import platform

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Relative_Path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
os_res = platform.system()

# os文件路径判断
if os_res == 'Windows':
    data_path = os.path.join(BASE_DIR + '\db')
    ftp_path = os.path.join(BASE_DIR + '\db\pub')
    path_file = os.path.join(BASE_DIR + '\db\\user_path\path')
    bin_path = os.path.join(BASE_DIR+'\\bin')
else:
    data_path = os.path.join(BASE_DIR + '/db')
    ftp_path = os.path.join(BASE_DIR + '\db\pub')
    path_file = os.path.join(BASE_DIR + '/db/user_path/path')
    bin_path = os.path.join(BASE_DIR + '/bin')

# path用户路径文件
if os.path.exists(path_file):
    with open(path_file, 'r', encoding='utf-8')as f:
        file = f.readlines()
        if len(file):
            file_object = file[0]
        else:
            with open(path_file, 'w', encoding='utf-8')as f:
                f.write('touch something')
                f.close()
else:
    with open(path_file, 'w', encoding='utf-8')as f:
        f.write('touch something')
        f.close()