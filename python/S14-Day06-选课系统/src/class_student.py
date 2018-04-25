#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Colin Yao
class Student(object):
    def __init__(self,student_name,student_gender,student_age,student_score):
        #学生性命,性别,年龄,分数
        self.student_name = student_name
        self.student_gender = student_gender
        self.student_age = student_age
        self.student_score = student_score
        self.student_classroom = {}