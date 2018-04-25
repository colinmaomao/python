#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Colin Yao
import os,sys,json,logging
"""ATM 信用卡后台manger_account 创建、锁定、提升额度"""
BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR) #添加环境变量
import json,sys,os,logging,time,datetime
from core import auth
"""添加信用卡,冻结信用卡,提升信用卡额度"""

"""管理接口调用"""

"""添加信用卡账户"""
def issue():
    creditcard_user = input("需要添加发行的信用卡的用户:>>>:")
    personinfo_input = input("使用人>>>:")
    _db_creditcard_record = BASE_DIR + r"\db\accounts\%s_creditcard_dict" % creditcard_user
    _db_creditcard_record_bak = BASE_DIR + r"\db\accounts\%s_creditcard_dict_bak" % creditcard_user
    _db_creditcard_record1 = BASE_DIR + r"\db\accounts\%s_creditcard_record" % creditcard_user
    usertype = {
    creditcard_user:{
    "creditcard":creditcard_user,
    "personinfo":personinfo_input,
    "password":'123',#默认密码123
    "limit": float('15000'),#默认额度
    "deflimit":float('15000'),
    "limitcash":float("7500"),
    "locked":"0"
    }}
    creditcard_value= {creditcard_user:{ "":{ "":""}}} #初始化一个流水字典
    res = os.path.exists(_db_creditcard_record)
    if res == True:
        print("用户已经存在")
    else:
       f = open(_db_creditcard_record,'w',encoding='utf-8')
       list = json.dumps(usertype)
       f.write(list)
       f.close()
       f1 = open(_db_creditcard_record1,'w',encoding='utf-8')
       list1 = json.dumps(creditcard_value)
       f1.write(list1)
       f1.close()
       print("添加用户成功")

"""冻结账户"""

def frozen():
    creditcard_user = input("需要冻结发行的信用卡的用户:>>>:")
    _db_creditcard_record = BASE_DIR + r"\db\accounts\%s_creditcard_dict" % creditcard_user
    _db_creditcard_record_bak = BASE_DIR + r"\db\accounts\%s_creditcard_dict_bak" % creditcard_user
    res = os.path.exists(_db_creditcard_record)
    if res != True:
        print("用户不存在请重新输入存在")
    else:
        f = open(_db_creditcard_record, 'r', encoding='utf-8')
        list = json.loads(f.read())
        a = list[creditcard_user]["locked"]
        f.close()
        if a != '0':
            print("用户已经被冻结")
        else:
            f1 = open(_db_creditcard_record_bak, 'w', encoding='utf-8')
            list[creditcard_user]["locked"] = '1'
            dict = json.dumps(list)
            f1.write(dict)
            f1.close()
            os.remove(_db_creditcard_record)
            os.rename(_db_creditcard_record_bak, _db_creditcard_record)
            print("冻结成功信用为:%s" %creditcard_user)

"""提升信用卡额度"""

def promotion_quota():
    creditcard_user = input("需要提额的信用卡的用户:>>>:")
    _db_creditcard_record = BASE_DIR + r"\db\accounts\%s_creditcard_dict" %creditcard_user
    _db_creditcard_record_bak = BASE_DIR + r"\db\accounts\%s_creditcard_dict_bak" %creditcard_user
    res = os.path.exists(_db_creditcard_record)
    if res != True:
        print("用户不存在请重新输入存在")
    else:
        f = open(_db_creditcard_record, 'r', encoding='utf-8')

        list = json.loads(f.read())
        deflimit = list[creditcard_user]["deflimit"]
        print("现有额度为%s"%deflimit)
        def_creditcard_user_cash = input("请输入要提升的额度>>>:") #这里提升的额度为deflimit
        creditcard_limit = (int(def_creditcard_user_cash) -  int(deflimit) + int(list[creditcard_user]["limit"] ))          #固定额度减去提升的额度、加上现有额度、提升后的信用卡额度
        creditcard_limitcash = (int(list[creditcard_user]["limitcash"]) + ((int(def_creditcard_user_cash) -  int(deflimit))* 0.5))  #提升后的额度 - 原有的固定额度*0.5 + 现在的取现额度才是提升后的取现额度 ：（  MMP!!!!!!!!!!!!!!!
        list[creditcard_user]["deflimit"] = def_creditcard_user_cash  #提升后的固定额度写入字典
        list[creditcard_user]["limit"] = creditcard_limit #提升固定额度后的信用卡额度写入字典
        list[creditcard_user]["limitcash"] = creditcard_limitcash #提升固定额度后的取现额度写入字典
        a = list[creditcard_user]["locked"]
        f.close()
        if a != '0':
            print("用户已经被冻结.不能提额")
        else:
            f1 = open(_db_creditcard_record_bak, 'w', encoding='utf-8')
            dict = json.dumps(list)
            f1.write(dict)
            f1.close()
            os.remove(_db_creditcard_record)
            os.rename(_db_creditcard_record_bak, _db_creditcard_record)
            print("成功提升信用额度为:%s 提额后的现有额度:%s 提升后的取现额度 %s " % (
            def_creditcard_user_cash, creditcard_limit, creditcard_limitcash))

