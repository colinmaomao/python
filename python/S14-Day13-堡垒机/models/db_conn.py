#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Time:2017/12/15 23:21
__Author__ = 'Sean Yao'
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from conf import settings

engine = create_engine(settings.ConnParams)
# 创建与数据库的会话session class ,注意,这里返回给session的是个class,不是实例
SessionCls = sessionmaker(bind=engine)
session = SessionCls()
