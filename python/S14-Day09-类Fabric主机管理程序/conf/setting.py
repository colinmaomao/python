#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Colin Yao
'''配置文件'''
import os
import sys
import platform

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

if platform.system() == 'Windows':
    server_list_path = os.path.dirname(os.path.abspath(__file__))+'\\'+'server_list'#主机列表字典路径变量
    server_dict_path = os.path.dirname(os.path.abspath(__file__)) + '\\' + 'server_dict'
    download_path = (base_dir+'\\'+'db\download') #下载路径变量
    upload_path = (base_dir + '\\' + 'db\\upload') #上传路径变量
else:
    server_list_path = os.path.dirname(os.path.abspath(__file__)) + '/' + 'server_list'
    server_dict_path = os.path.dirname(os.path.abspath(__file__)) + '/' + 'server_dict'
    download_path = (base_dir + '/' + 'db\download')
    upload_path = (base_dir + '/' + 'db\\upload')