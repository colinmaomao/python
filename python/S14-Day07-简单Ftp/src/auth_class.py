#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Colin Yao
class Auth(object):
    '''用户验证类类为用户、密码家目录'''
    def __init__(self,name,passwd):
        self.name = name
        self.passwd = passwd
