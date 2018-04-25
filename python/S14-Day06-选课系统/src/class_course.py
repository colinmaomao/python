#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Colin Yao
'''课程类'''
import time
class Course(object):
    def __init__(self,course_name,course_price,course_time):
        self.course_name = course_name
        self.course_price = course_price
        self.course_time = course_time
