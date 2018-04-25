#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Colin Yao
import os
import sys
import pickle
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
from conf import setting

def basic_dict():
    '''
    初始化程序字典
    :return:
    '''
    add_machine_dict = {'machine': {'group1': {'192.168.84.130': {'ip': '192.168.84.130', 'port': '12321', 'username':
                        'root', 'passwd': '123456'}}}}
    with open(setting.server_list_path, 'wb') as dict_file_object:
        dict_file_object.write(pickle.dumps(add_machine_dict))
        dict_file_object.close()