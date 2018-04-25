#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Colin Yao
'''
用户验证基础类
'''
class Auth(object):
    '''
    验证类
    '''
    def __init__(self,name,passwd):
        '''
        构造方法
        :param name: 用户名
        :param passwd: 密码
        '''
        self.name = name
        self.passwd = passwd
