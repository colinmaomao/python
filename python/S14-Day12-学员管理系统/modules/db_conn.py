#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Time:2017/12/19 20:37
__Author__ = 'Sean Yao'

from sqlalchemy import create_engine, Table
from sqlalchemy.orm import sessionmaker
from conf import settings


engine = create_engine(settings.ConnParams)

SessionCls = sessionmaker(bind=engine)
session = SessionCls()