#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Colin Yao
import json,sys,os,logging,time,datetime
BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR) #添加环境变量
from core import auth
from core import logger
log_obj = logger.log('transaction')

"""用户接口调用"""

"""我的信用卡信息"""

def my_creditcard(creditcard_user):
    while True:
        _db_creditcard_record = BASE_DIR + r"\db\accounts\%s_creditcard_dict" % creditcard_user
        print("\33[32;0m我的信用卡信息\33[0m".center(40, "-"))
        with open(_db_creditcard_record, 'r', encoding='utf-8') as f:
            list = json.loads(f.read())
            #print(list)
            #print(list[creditcard_user]["limit"])
            print("卡号:\t[%s]\n额度:\t[¥%s]\n取现额度:\t[¥%s]\n持卡人:\t[%s]\n" %(creditcard_user,list[creditcard_user]["limit"],list[creditcard_user]["limitcash"],list[creditcard_user]["personinfo"]))
        if_back = input("\33[34;0m是否退出 返回[b]\33[0m:")
        if if_back == "b":
            break
"""信用卡流水记录"""

def flow(creditcard_user,value):
    _db_creditcard_record = BASE_DIR + r"\db\accounts\%s_creditcard_record" %creditcard_user
    with open(_db_creditcard_record, "r+",encoding='utf-8') as f:
        list = json.loads(f.read())
        month = time.strftime('%Y-%m-%d', time.localtime())
        times = time.strftime("%H:%M:%S")
        if str(creditcard_user) not in list.keys():
            list[creditcard_user] = {month: {times: value}}
            print(list[creditcard_user])
        else:
            if month not in list[creditcard_user].keys():
                list[creditcard_user][month] = {times: value}
            else:
                list[creditcard_user][month][times] = value
        """value类似还款转账"""
        dict = json.dumps(list)
        f.seek(0)
        f.truncate(0)
        f.write(dict)

"""查看信用卡流水"""

def see(creditcard_user):
  while True:
      _db_creditcard_record = BASE_DIR + r"\db\accounts\%s_creditcard_record" % creditcard_user
      with open(_db_creditcard_record, "r+", encoding='utf-8') as f:
          list = json.loads(f.read())
          if creditcard_user in list.keys():
              for key in list[creditcard_user]:
                  print("消费日期为>>>:", key)
              date = input("\n\33[34;0m流水查询 返回[b] / 输入消费的日期既可以查询[2000-01-01]\33[0m:")
              if date == 'b':
                  break
                  pass
              if date in list[creditcard_user].keys():
                  keys = sorted(list[creditcard_user][date])
                  print("\33[31;1m当前信用卡[%s] 交易记录>>>\33[0m" % (creditcard_user))
                  for key in keys:
                      print("\33[31;1m时间>>>:%s  %s\33[0m" % (key, list[creditcard_user][date][key]))
                  print("")
              else:
                  print("\33[31;0m输入的日期有误\33[0m\n")
          else:
              print("\33[31;0m信用卡 %s 还没有进行过消费\33[0m\n" % (creditcard_user))
              break

"""提现"""
def withdrawals(creditcard_user):
    _db_creditcard_record = BASE_DIR + r"\db\accounts\%s_creditcard_dict" % creditcard_user
    _db_creditcard_record_bak = BASE_DIR + r"\db\accounts\%s_creditcard_dict_bak" % creditcard_user
    limit_input = input("请输入提现金额>>>:")
    f = open(_db_creditcard_record, "r", encoding='utf-8')
    list=json.loads(f.read())
    cash_limit = list[creditcard_user]["limitcash"]  #能提现的额度
    limit = list[creditcard_user]["limit"] #当前额度
    interest = (int(limit_input) * 0.05)
    new_limit = (limit - int(limit_input)-interest)  #当前额度-提现金额-利息等于现在的额度
    print("现在取款的金额", limit_input)
    print("当前额度", limit)
    print("利息", interest)
    print("取现后的额度", new_limit)
    if cash_limit >= int(limit_input):  # 当取现额度大于等于取现金额的时候
        if cash_limit >= int(limit_input):  # 当取现额度大于等于取现金额的时候
            list[creditcard_user]["limit"] = new_limit
            f.close()
            f1 = open(_db_creditcard_record_bak, "w", encoding='utf-8')
            f1.seek(0)
            f1.truncate(0)
            dict = json.dumps(list)
            f1.write(dict)
            f1.close()
            os.remove(_db_creditcard_record)
            os.rename(_db_creditcard_record_bak, _db_creditcard_record)
            value = "\33[31;1m信用卡用户:%s取现金额:¥%s 成功\33[0m" % (creditcard_user, limit_input)
            value1 = "\33[31;1m信用卡利息:¥%s 现在额度为:¥%s \33[0m" % (interest, new_limit)
            print(value, value1, "\n")
            log_obj.info(
                "account:%s cash:%s limit:%s interest:%s OK" % (creditcard_user, limit_input, new_limit, interest))
            flow(creditcard_user, value)
        else:
            print("输入有误重新输入")
    else:
        print("提款金额大于默认提款额度了,You Can 联系后台中心提升提款额度")
    return limit_input

"""转账"""
def transfer_accounts(creditcard_user):
    _db_creditcard_record = BASE_DIR + r"\db\accounts\%s_creditcard_dict" % creditcard_user
    _db_creditcard_record_bak = BASE_DIR + r"\db\accounts\%s_creditcard_dict_bak" % creditcard_user
    while True:
        print("\33[32;0m转账\33[0m".center(40, "-"))
        if_trans = input("\n\33[34;0m是否进行转账 确定[y]/返回[b]\33[0m:")
        if if_trans == "y":
            transfer_input = input("请输入需要转账的账户>>>:")
            #transfer_input = '222222'
            _db_creditcard_record_transfer = BASE_DIR + r"\db\accounts\%s_creditcard_dict" %transfer_input
            _db_creditcard_record_bak_transfer = BASE_DIR + r"\db\accounts\%s_creditcard_dict_bak" %transfer_input
            transfer_cash_input = input("请输入需要转账的金额>>>:")#输入转出的金额
            #transfer_cash_input = '1000'
            f = open(_db_creditcard_record, "r", encoding='utf-8') #首先先确认这个金额是否超过额度，如果超过额度那么不能转账
            list = json.loads(f.read())  #
            limit = list[creditcard_user]["limit"]
            print("现在的额度%s 可转账金额%s" %(limit,limit))
            print("转账金额%s" %transfer_cash_input)
            if int(transfer_cash_input) <= limit:
                #用当前信用卡额度转账金额  limit - transfer_cache_input
                new_limit = (limit - int(transfer_cash_input))
                print("信用卡转账后的额度%s"%new_limit) #处理自己的额度然后处理转账账户的额度
                list[creditcard_user]["limit"] = new_limit
                f.close()
                f1 = open(_db_creditcard_record_bak, "w", encoding='utf-8')
                f1.seek(0)
                f1.truncate(0)
                dict = json.dumps(list)
                f1.write(dict)
                f1.close()
                os.remove(_db_creditcard_record)
                os.rename(_db_creditcard_record_bak,_db_creditcard_record)
                value = "\33[31;1m信用卡 %s 转账金额 ¥%s 转账成功\33[0m" % (creditcard_user,transfer_cash_input)
                print(value, "\n")
                log_obj.info("account:%s transfer_account:%s  cash:%s limit:%s OK" %(creditcard_user,transfer_input,transfer_cash_input,new_limit,))
            else:
                print("还款额大于默认额度了，可以联系后台中心提升默认额度")
            flow(creditcard_user, value)
            #处理对方账户的金额
            if transfer_input in _db_creditcard_record_transfer:
                f2 = open(_db_creditcard_record_transfer, "r", encoding='utf-8')  # 打开转账用户的文件
                list1 = json.loads(f2.read())  #
                limit2 = list1[transfer_input]["limit"]  #对方的信用卡额度
                new_limit1 = (limit2 + int(transfer_cash_input)) #准备增加对方信用卡额度
                list1[transfer_input]["limit"] = new_limit1
                f2.close()
                f3 = open(_db_creditcard_record_bak_transfer, "w", encoding='utf-8')
                f3.seek(0)
                f3.truncate(0)
                dict1 = json.dumps(list1)
                print()
                f3.write(dict1)
                f3.close()
                os.remove(_db_creditcard_record_transfer)
                os.rename(_db_creditcard_record_bak_transfer, _db_creditcard_record_transfer)
        if if_trans == "b":
            break

"""还款"""
def repayment(creditcard_user):
    _db_creditcard_record = BASE_DIR + r"\db\accounts\%s_creditcard_dict" % creditcard_user
    _db_creditcard_record_bak = BASE_DIR + r"\db\accounts\%s_creditcard_dict_bak" % creditcard_user
    limit_input = input("请输入还款金额>>>:")
    f = open(_db_creditcard_record, "r", encoding='utf-8')
    list=json.loads(f.read())
    limit = list[creditcard_user]["limit"]
    deflimit = list[creditcard_user]["deflimit"]
    new_limit = (limit + int(limit_input))
    if int(new_limit) <= int(deflimit):
        list[creditcard_user]["limit"] = new_limit
        f.close()
        f1 = open(_db_creditcard_record_bak, "w", encoding='utf-8')
        f1.seek(0)
        f1.truncate(0)
        dict = json.dumps(list)
        f1.write(dict)
        f1.close()
        os.remove(_db_creditcard_record)
        os.rename(_db_creditcard_record_bak,_db_creditcard_record)
        value = "\33[31;1m信用卡 %s 还款金额 ¥%s 还款成功\33[0m" % (creditcard_user, limit_input)
        log_obj.info("account:%s repayment:%s limit:%s OK" % (creditcard_user, limit_input, new_limit))
        print(value, "\n")
        flow(creditcard_user, value)
    else:
        print("还款额大于默认额度了，可以联系后台中心提升默认额度")
        pass