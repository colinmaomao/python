#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Colin Yao
"""#ATM管理接口"""
import os,sys
BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR) #添加环境变量
from core import auth
from core import accounts
from core import creditcard
from conf import settings


"""输入账号密码创建超级用户"""

msg =  '''
\33[34;0m
欢迎进入ATM后台管理接口

[1] 添加信用卡
[2] 冻结信用卡
[3] 提升信用卡额度
[4] 退出
\33[0m
'''

"""输入用户选择调用account模块"""

def user_choice():
    while True:
        print(msg)
        user_choice = input("请输入模式进行操作>>>:")
        if user_choice == '1':
            # 调用account模块的issue函数添加用户
            accounts.issue()
        elif user_choice == '2':
            # 调用account模块的fozen函数锁定用户
            accounts.frozen()
        elif user_choice == '3':
            # 调用account模块的un_lock函数解锁用户
            accounts.promotion_quota()
        elif user_choice == '4' or user_choice == 'q':
            sys.exit()
        else:
            print("输入有误，程序退出")
            sys.exit()
"""程序入口"""
def manage():
    auth.admincenter_auth() # 调用用户认证auth模块中manger函数1 默认账户密码admin shopping_db
    user_choice()
manage()