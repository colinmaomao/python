#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Time:2017/12/17 17:57
__Author__ = 'Sean Yao'
import os
import codecs
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import models
import redis
import re
#
# pool = redis.ConnectionPool(host='192.168.84.66', port=6379)
# # redis 每次连接消耗很大，可以搞一个连接池
# r = redis.Redis(connection_pool=pool)
# s = r.lrange('Sean_user_record', 0, -1)
# cmd_caches = []
# for i in s:
#     v = i.decode().replace('[', '').replace(']', '').split(',')
#     v2 = v[3].replace("'", '').encode().decode()
#     print(v[0], v[1], v[2], v2, v[4].replace("'", ''))
#     print(codecs.getdecoder("unicode_escape")(v[3])[0])

# f = 'find\x08\t\x07d -name adsa'
# print(re.sub('\s', '|', f.encode().decode('unicode-escape')))
# print(f.encode().decode('unicode-escape'))


#print(codecs.getdecoder("unicode_escape")('asdsdadas\tASDASD\t\t')[0])
    # 转一下字符 1  6  'cmd'   \x08f\x08df -TH  2017-12-17 22:18:04
# print('\x08f\x08df -TH')
# key_name = 'a'+'login'
# print(key_name)
# s = r.lrange('1login', 0, -1)
# print(s[0].decode())

# import sqlalchemy
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import Column, Integer, String
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy import func
#
# engine = create_engine("mysql+pymysql://root:123456@192.168.84.66/tinydb",
#                        encoding='utf-8')  # ,echo=True)
# Base = declarative_base()
# Session_class = sessionmaker(bind=engine)
# Session = Session_class()
#
# # 查询
# data = Session.query().filter_by().all()  # all取一个列表，first取第一个
# print(data)