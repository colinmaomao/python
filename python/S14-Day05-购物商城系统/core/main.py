#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Colin Yao
import os,sys,logging,json
BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR) #添加环境变量
from core import logger
from core import auth
from core import creditcard

def center():
    msg = '''
        \33[34;0m
        [1]我的信用卡
        [2]信用卡流水记录
        [3]提现
        [4]转账
        [5]还款
        [6]退出按q 即可
        \33[0m
        '''
    print("欢迎进入信用卡ATM中心请输入账号名密码进行认证")
    res = auth.creditcard_auth()
    creditcard_user = res[1]
    while True:
        print(msg)
        choice_id = input("请选择您需要的服务>>>:")
        if choice_id == "1":
            creditcard.my_creditcard(creditcard_user)
        elif choice_id == "2":
            creditcard.see(creditcard_user)
        elif choice_id == "3":
            creditcard.withdrawals(creditcard_user)
        elif choice_id == "4":
            creditcard.transfer_accounts(creditcard_user)
        elif choice_id == "5":
            creditcard.repayment(creditcard_user)
        elif choice_id == "6" or choice_id == "q":
            print("Bye %s" % creditcard_user)
            sys.exit()
        else:
            print("输入有误请重新输入")
center()