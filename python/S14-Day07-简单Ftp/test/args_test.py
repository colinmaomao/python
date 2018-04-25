# #!/usr/bin/env python
# # -*- coding:utf-8 -*-
# # Author: Colin Yao
# import os
# # print(os.user_path.isfile(r"E:\S14\HomeWork\S14-Day07-简单Ftp\db\colin\colin\xtest"))
# #
# # print(os.user_path.isdir(r"E:\S14\HomeWork\S14-Day07-简单Ftp\db\colin"))
# #
# # a = b'Python\\xe4\\xb8\\x89\\xe7\\xba\\xa7\\xe8\\x8f\\x9c\\xe5\\x8d\\x95\\xe4\\xbd\\x9c\\xe4\\xb8\\x9a.png'
# # a.decode().encode()
# # print(a)
# class Aa(object):
#     def __init__(self):
#         msg = input('请输入命令>>>:')
#         #if len(msg) == 0: continue
#         (cmd, file_name) = msg.strip().split(' ')
#         self.list = {}
# Author: Colin Yao
# import logging
# os_res = platform.system()
# if  os_res == 'Windows':
#     data_path = os.user_path.join(BASE_DIR + '\db')
#     path_file = os.user_path.join(BASE_DIR + '\db\user_path')
#     cmd_file = os.user_path.join(BASE_DIR + '\db\cmd')
# else:
#     data_path = os.user_path.join(BASE_DIR + '/db')
#     path_file = os.user_path.join(BASE_DIR + '/db/user_path')
#     cmd_file = os.user_path.join(BASE_DIR + '/db/cmd')
#
#
# f = open(cmd_file, 'r', encoding='utf-8')  # 将上传的文件传递到用户的目录下
# cmd = f.readlines()
# print(cmd)
# import os,sys,shelve,subprocess,platform
# BASE_DIR  = os.user_path.dirname(os.user_path.dirname(os.user_path.abspath(__file__)))
# sys.user_path.append(BASE_DIR) #添加环境变量
# import  pickle,json
# from conf import setting
# f = open(setting.cmd_file, 'rb')  # 读取字典操作
# user_list = js.loads(f)
# f.close()
# import os
# os.user_path.getatime('')