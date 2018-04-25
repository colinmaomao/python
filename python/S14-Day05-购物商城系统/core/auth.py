#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Colin Yao
import os,sys,json
BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR) #添加环境变量
super_user_passwd = BASE_DIR + r"\db\accounts\super_user_passwd"
from core import logger
def auth(auth_type):
    """超级用户后台管理认证接口"""
    def outer_wrapper(func):
        if auth_type =="admincenter_auth":
            def wrapper():
                res = func()
                super_user = input("请输入后台管理员账号>>>>:")
                super_passwd = input("请输入后台管理员密码>>>>:")
                with  open(super_user_passwd, 'r', encoding='utf-8') as f:
                    (id, user, passwd) = f.readline().strip().split(',')
                if user == super_user and passwd == super_passwd:
                    print("welcome %s" %super_user)
                    return res,super_user
                else:
                    log_obj = logger.log('access')
                    log_obj.error("不正确的密码 %s" % super_user)
                    print("用户名或密码输入有误程序退出")
                    sys.exit()
            return wrapper

        """商城用户登录认证"""
        if auth_type == "user_auth":
            def wrapper():
                res = func()
                shopping_user = input("请输入用户名>>>>:")
                shopping_passwd = input("请输入密码>>>>:")
                print("功能后面在加入")
                # with  open(super_user_passwd, 'r', encoding='utf-8') as f:
                #     f.readlines()

            return wrapper
        if auth_type == "creditcard_auth":
            def wrapper():
                log_obj = logger.log('access')
                res = func()
                creditcard_user = input("请输入信用卡账号>>>>:")  # 信用卡账号
                creditcard_passwd = input("请输入信用卡密码>>>>:")  # 信用卡密码
                _creditcard_passwd = BASE_DIR + r"\db\accounts\%s_creditcard_dict" % creditcard_user
                res = os.path.exists(_creditcard_passwd)
                if res == True:
                    if len(creditcard_user.strip()) > 0:
                        with open(_creditcard_passwd, 'r', encoding='utf-8') as f:
                            list = json.loads(f.read())
                            if creditcard_user in list.keys():  # 用户在key中、用户唯一
                                if creditcard_passwd == list[creditcard_user]["password"]:  # 读取字典中用户和key的值
                                    if list[creditcard_user]["locked"] == '0':  # 如果用户的lock 为0 证明是没有锁定的账户为1 是锁定状态
                                        print("信用卡认证成功 welcome %s" % creditcard_user)
                                        return res,creditcard_user
                                    else:
                                        print("信用卡被冻结用户%s请您联系用户中心 WEB：扯淡.com  TEL： 100000" % creditcard_user)
                                        log_obj.error("%s is locked" % creditcard_user)
                                        sys.exit()
                                else:
                                    print("信用卡用户:%s 密码输入有误认证失败" % creditcard_user)
                                    log_obj.error("%s wrong shopping_db " % creditcard_user)
                                    sys.exit()
                            else:
                                sys.exit()
                    else:
                        sys.exit()
                else:
                    print("不存在此信用卡用户%s" % creditcard_user)
                    log_obj.error("%s wrong username" % creditcard_user)
                    sys.exit()
            return wrapper
    return outer_wrapper

"""装饰器添加print语句并带有色彩"""

'''后台管理认证'''
@auth(auth_type="user_auth")
def user_auth():
    print("\33[32;0m用户登录认证\33[0m".center(40,"-"))
    return "True"

'''信用卡认证'''
@auth(auth_type="creditcard_auth")
def creditcard_auth():
    print("\33[32;0m信用卡登录认证\33[0m".center(40,"-"))
    return "True"

'''后台管理认证'''
@auth(auth_type="admincenter_auth")
def admincenter_auth():
    print("\33[32;0m后台管理登录认证\33[0m".center(40,"-"))
    return "True"