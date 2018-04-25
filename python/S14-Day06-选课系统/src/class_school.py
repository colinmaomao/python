#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Colin Yao
import  time,os,shelve,sys
BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR) #添加环境变量
from src.class_teacher import Teacher
from src.class_course import Course
from src.class_classroom import Class_room
from src.class_student import Student
'''学校类'''
class School(object):
    def __init__(self,school_name,school_addr):
        self.school_name  = school_name
        self.school_addr  = school_addr
        self.school_course = {}
        self.sch_class_room ={}
        self.sch_teacher = {}
        self.sch_student = {}

        '''创建课程'''
    def create_course(self,course_name,course_price,course_time):
        course_obj = Course(course_name,course_price,course_time) #创建课程对象
        self.school_course[course_name] = course_obj  #根据课程名为key,课程对象为value创建对应关系传进了init self.school_course

        '''展示课程'''
    def show_course(self):
        for course in self.school_course:
            course_obj = self.school_course[course]
            print(course_obj.__dict__)  #是否需要添加学校
            print('所在分校:%s\t课程名称:%s\t课程价格:%s\t课程学习计划:%s周'
                  %(self.school_addr,course_obj.course_name,course_obj.course_price,course_obj.course_time))

        '''修改课程'''
    def modify_course(self):  #可能会继续追加、保留
        for course in self.school_course:
            course_obj = self.school_course[course]
            course_obj.course_name= input('修改课程名称>>>:')
            course_obj.course_price = input('修改课程价格>>>:')
            course_obj.course_time = input('修改课程周期>>>:')

        '''创建教室'''
    def create_classroom(self,class_name,course_obj): #创建classroom、关联课程
        class_obj = Class_room(class_name,course_obj) #创建课程对象
        self.sch_class_room[class_name] = class_obj  #根据教室名为key,课程对象为value创建对应关系传进了init self.school_course

        '''展示教室'''
    def show_classroom(self):
        for classroom in self.sch_class_room:
            class_obj = self.sch_class_room[classroom]
            #应该是班级名称、对应课程、对应老师、对应的student、保留
            print('班级名称:%s\t课程:%s'
                  % (class_obj.class_name,class_obj.course_obj))
            print(class_obj.__dict__)

        '''修改教室'''
    def modify_course(self):  #可能会继续追加、保留
        for classroom in self.sch_class_room:
            class_obj = self.sch_class_room[classroom]
            x = time.strftime("%Y%m%d%H%M%S", time.localtime()) #按照根据时间修改教室省去输入
            class_obj.course_obj = input('请慎重输入课程名称>>>:')
            y = time.strftime("%Y%m%d%H%M%S", time.localtime())
            class_obj.class_name= (y+"_"+ class_obj.course_obj)

        '''创建教师'''
    def create_teacher(self,teacher_name,teacher_age,teacher_gender,teacher_salary,class_name,class_obj):
        teacher_obj = Teacher(teacher_name,teacher_age,teacher_gender,teacher_salary)
        teacher_obj.add_tech_classroom(class_name,class_obj)   #讲师关联教室
        self.sch_teacher[teacher_name] = teacher_obj

        '''查看教师'''
    def show_teacher(self):
        for teacher_name in self.teacher:
            teacher_obj=self.teacher[teacher_name]
            print('老师姓名:%s','老师年龄:%s','老师性别:%s','老师工资:%s'
                  %(teacher_obj.teacher_name,teacher_obj.teacher_age,teacher_obj.teacher_gender,teacher_obj.teacher_salary))

        '''修改老师'''
    def modify_teacher(self):
        for teacher_name in self.teacher:
            teacher_obj=self.teacher[teacher_name]
            teacher_obj.teacher_name = input('请输入修改的老师姓名>>>:')
            teacher_obj.teacher_age = input('请输入修改的老师年龄>>>:')
            teacher_obj.teacher_gender = input('请输入修改的老师性别>>>:')
            teacher_obj.teacher_salary = input('请输入修改的老师工资>>>:')

        '''创建学生'''
    def create_student(self,student_name,student_gender,student_age,student_score,class_name):
       #创建学生对象
       student_obj = Student(student_name,student_gender,student_age,student_score)
       self.sch_student[student_name] = student_obj
       #建立学生和班级的关联关系
       class_obj = self.sch_class_room[class_name]
       class_obj.class_student[student_name] = student_obj
       #更新班级信息
       self.sch_class_room[class_name] =class_obj


