#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Colin Yao
import  time
'''班级类'''
class Class_room(object):
    def __init__(self,class_name,course_obj):
        self.class_name = class_name
        self.course_obj = course_obj
        self.class_student = {}
