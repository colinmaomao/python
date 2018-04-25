#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Colin Yao
import os,sys,logging,shelve
BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR) #添加环境变量
from conf import setting
from core.school_view import School_view
from core.teacher_view import Teacher_view
from core.student_view import Student_view

class Admin(object):
    def run(self):
        exit_flag =False
        menu = u'''
        \033[32;1m
        1.学生视图
        2.老师视图
        3.学校视图
        4.退出\033[0m
        '''
        while not exit_flag:
            print(menu)
            user_option = input('请输入要管理的视图,输入q退出>>>:\t')
            if user_option == '1':
                Student_view()
            elif user_option == '2':
                Teacher_view()
            elif user_option == '3':
                School_view()
            elif user_option == 'q' or user_option =='4':
                sys.exit()
            else:
                print('输入的选项不正确,请重新输入')
