#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Colin Yao
'''主配置文件'''
import os
import sys
import platform
BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

if platform == 'Windows':#添加上传下载目录变量
    download_path =  (BASE_DIR+'\\'+"\db"+"\Server_DownLoad")
    upload_path = (BASE_DIR+'\\'+"\db"+"\\Server_Upload")
    client_download_path = (BASE_DIR+'\\'+"\db"+"\Client_DownLoad")
else:
    download_path =  (BASE_DIR+'/'+"/db"+"/Server_DownLoad")
    upload_path = (BASE_DIR+'/'+"/db"+"/Server_Upload")
    client_download_path = (BASE_DIR + '/' + "/db" + "/Client_DownLoad")
