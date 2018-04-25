#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Colin Yao
#配置文件
import logging
import os,sys

BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR) #添加环境变量

LOGIN_LEVEL = logging.INFO#定义日志的记录级别

#print(DATABASE)
#日志类型
LOGIN_TYPE={
    "access":"access.logs",
    "transaction":"transaction.logs"
}

# DATABASE = {
#     "db_tool":"file_storage",  #文件存储，这里可拓展成数据库形式的
#     "name":"accounts",         #db下的文件名
#     "user_path":"%s/src"%BASE_DIR
# }
#shopping

