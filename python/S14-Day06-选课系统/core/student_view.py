#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Colin Yao
import os, sys, logging, shelve

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)  # 添加环境变量
from conf import setting
from src.class_school import School
from core.school_view import School_view

class Student_view(object):
    def __init__(self):
        if os.path.exists(setting.school_file+ '.dat'):
            self.school_file = shelve.open(setting.school_file)
            self.student_manger()
            self.school_file.close()
        else:
            print('没有数据,请联系管理员选择分校')
            sys.exit()
    def student_manger(self):
        while True:
            print('欢迎注册IT学院我们的分校有:')
            for school_name in self.school_file:
                print('\tSean[%s]分校' %school_name)
            school_option = input('请输入您要学习的分校地址>>>:').strip()

            if school_option in self.school_file:
                self.school_option = school_option
                self.school_obj = self.school_file[school_option]
            else:
                print('输入有误程序退出')
                sys.exit()
            for classroom in self.school_obj.sch_class_room:
                class_obj = self.school_obj.sch_class_room[classroom]
                print('欢迎来到%s分校我们的班级有:%s\t课程有:%s'
                      % (school_option, class_obj.class_name, class_obj.course_obj.course_name))

            student_option = input('请输入学生姓名进行操作[PS:注册也在这里哟]>>>:').strip()
            if student_option in self.school_obj.sch_student:
                self.student_option = student_option
                self.student_obj = self.school_obj.sch_student[self.student_option]
            else:
                print('[%s]这位童鞋'%student_option,'您是否进行注册?')
                user_choice = input('请注册/退出(y/n)>>>:')
                if user_choice == 'y':
                    self.student_option = student_option
                    self.enroll()
                elif user_choice == 'n':
                    sys.exit()
                else:
                    print('输入有误,请重新开始 = 。= ')
                    self.student_manger()
            while True:
                menu = '''
                          欢迎来到       Python[%s]校区[%s]童鞋
                          缴纳学费       pay
                          选择教室/课程  choice_class
                          查看讲师       view_teacher
                          退出           exit
                          ''' %(school_option,student_option)
                print(menu)
                user_choice = input('请选择以上操作>>>:').strip()
                if hasattr(self, user_choice):
                    getattr(self, user_choice)()
                else:
                    print("没有这个操作,请重新输入!!!!")
                    pass

    '''注册'''
    def enroll(self):  # 课程、班级
        student_name = self.student_option
        student_gender = input('%s童鞋请输入性别>>>:' % student_name)
        student_age = input('%s童鞋请输入年纪>>>:' % student_name)
        class_name = input('%s童鞋请输入教室(PS:教室已经和课程关联)>>>:' % student_name)
        student_score = None
        if class_name in self.school_obj.sch_class_room:
            class_obj = self.school_obj.sch_class_room[class_name]
            self.school_obj.create_student(student_name, student_gender, student_age, student_score, class_name)
            self.school_file.update({self.school_option: self.school_obj})
            self.school_file.close()
            print('%s童鞋注册成功,您选择的课程是%s,教室为%s'
                  % (student_name, class_obj.course_obj.course_name, class_obj.class_name))
        else:
            print('创建失败教室不存在')

    '''缴纳学费'''

    def pay(self):  # 根据教室缴纳学费
        student_name = self.student_option
        class_name = input('%s童鞋请输入您所在的教室(PS:教室已经和课程关联)>>>:' % student_name)
        if class_name in self.school_obj.sch_class_room:  # sch_class_room
            class_obj = self.school_obj.sch_class_room[class_name]
        if class_obj.course_obj.course_name in self.school_obj.school_course:
            course_obj = self.school_obj.school_course[class_obj.course_obj.course_name]
            print('所在分校:%s\t课程名称:%s\t课程价格:%s\t课程学习计划:%s周'
                  % (self.school_obj.school_addr, course_obj.course_name, course_obj.course_price, course_obj.course_time))

    '''选择班级'''
    def choice_class(self):  # 根据学习日期选择班级
        student_name = self.student_option
        student_gender = self.student_obj.student_gender
        student_age = self.student_obj.student_age
        class_name = input('%s童鞋选择教室(PS:教室已经和课程关联)>>>:' % student_name)
        student_score = 0
        # class_name ='room'
        if class_name in self.school_obj.sch_class_room:  # sch_class_room
            class_obj = self.school_obj.sch_class_room[class_name]
            self.school_obj.create_student(student_name, student_gender, student_age, student_score, class_name)
            self.school_file.update({self.school_option: self.school_obj})
            self.school_file.close()
            print('%s更改教室成功,您选择的课程是%s,教室为%s'
                  % (student_name, class_obj.course_obj.course_name, class_obj.class_name))
        else:
            print('创建失败教室不存在')

    '''查看讲师'''
    def view_teacher(self):
        for teacher_name in self.school_obj.sch_teacher:
            teacher_obj = self.school_obj.sch_teacher[teacher_name]
            for t in teacher_obj.teacher_classroom:
                class_obj = self.school_obj.sch_class_room[t]
                stu_list = []
                for j in class_obj.class_student:
                    stu_list.append(j)
                print('教师姓名:%s\t教师所在班级:%s\t教授课程:%s\t学生有%s'
                      % (teacher_obj.teacher_name,t, class_obj.course_obj.course_name,stu_list))
    '''退出'''
    def exit(self):
        sys.exit('感谢使用再见')