#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Colin Yao
import os,sys,logging,shelve
BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR) #添加环境变量
from conf import setting
from src.class_school import School

class School_view(object):
    def __init__(self):
        if os.path.exists(setting.school_file+ '.dat'):
            self.school_file = shelve.open(setting.school_file)
            self.school_manger()
            self.school_file.close()
        else:
            print('没有学校和班级的数据,请先创建')
            self.init_school()
            self.school_manger()
            self.school_file.close()
    def init_school(self):
        self.school_file = shelve.open(setting.school_file)
        self.school_file['北京'] = School('总校','北京')
        self.school_file['上海'] = School('总校','上海')

    def school_manger(self):
        while True:
            for school_name in self.school_file:
                print('学校名称:%s'%school_name)
            school_option = input('请输入要管理的学校名称>>>:').strip()
            if school_option in  self.school_file:
                self.school_option = school_option
                self.school_obj = self.school_file[school_option]
                '''
                如果是北京就等于self.school_obj[北京]
                file[北京] =School('总校','北京')
                所以当下文出现了self.school_obj.school_course =School('总校','北京').school_course
                等同于调用了School().school_course的属性是
                '''
            while True:
                menu = '''
                欢迎来到  Python%s校区
                添加课程  add_course
                添加班级  add_classroom
                添加讲师  add_teacher
                查看班级  show_classroom
                查看课程  show_classroom
                查看讲师  show_teacher
                修改讲师  add_teacher
                退出      exit
                '''%school_option
                print(menu)
                user_choice = input('请选择以上操作>>>:').strip()
                if hasattr(self,user_choice):
                    getattr(self,user_choice)()
                else:
                    print("没有这个操作,请重新输入!!!!")
                    pass

    def add_course(self):
        course_name = input('请输入课程名称>>>:').strip()
        course_price = input('请输入课程价格>>>:').strip()
        course_time = input('请输入课程周期[默认为周]>>>:').strip()
        if course_name in self.school_obj.school_course:
            print('课程已经存在')
        else:
            self.school_obj.create_course(course_name, course_price, course_time)  #相当于School.create_course(course_name, course_price, course_time)
            print('%s课程添加成功' % course_name)
        self.school_file.update({self.school_option:self.school_obj})
        self.school_file.close()

    def add_classroom(self):
        class_name = input('请输入班级名称>>>:').strip()
        class_course = input('请输入课程>>>:').strip()
        if class_name not in self.school_obj.sch_class_room:    #sch_class_room
            if class_name not in self.school_obj.school_course:
                course_obj = self.school_obj.school_course[class_course]
                self.school_obj.create_classroom(class_name,course_obj)
                self.school_file.update({self.school_option:self.school_obj})
                self.school_file.close()
                print('班级创建成功')
            else:
                print('课程不存在')
        else:
           print('班级已经存在')

    def show_classroom(self):
        for classroom in self.school_obj.sch_class_room:
            class_obj = self.school_obj.sch_class_room[classroom]
            print('班级名称:%s\t课程:%s'
                  % (class_obj.class_name,class_obj.course_obj.course_name))

    def add_teacher(self):
        teacher_name = input('请输入讲师姓名>>>:')
        teacher_age = input('请输入讲师年龄>>>:')
        teacher_gender = input('请输入讲师性别>>>:')
        teacher_salary = input('请输入讲师薪水>>>:')
        class_name = input('请输入授课班级>>>:')

        if class_name in self.school_obj.sch_class_room:  # sch_class_room
            class_obj = self.school_obj.sch_class_room[class_name]
            if teacher_name not in self.school_obj.sch_teacher:
                self.school_obj.create_teacher(teacher_name,teacher_age,teacher_gender,teacher_salary,class_name,class_obj)
                print('讲师创建成功,请确认是否已经签完合同')
            else:
                self.school_obj.modify_teacher({})
                print('修改讲师成功')
            self.school_file.update({self.school_option:self.school_obj})
            self.school_file.close()
        else:
            print('请先创建班级')

    def show_teacher(self):
        for teacher_name in self.school_obj.sch_teacher:
            teacher_obj = self.school_obj.sch_teacher[teacher_name]
            for t in teacher_obj.teacher_classroom:
                class_obj =  self.school_obj.sch_class_room[t]
                stu_list = []
                for j in class_obj.class_student:
                    stu_list.append(j)
                print('教师姓名:%s\t教师所在班级:%s\t教授课程:%s\t课程学员:%s' %(teacher_obj.teacher_name
                                                               ,t,class_obj.course_obj.course_name,stu_list))
    def exit(self):
        sys.exit('程序退出')