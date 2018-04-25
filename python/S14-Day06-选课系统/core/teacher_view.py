#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Colin Yao
import os,sys,logging,shelve
BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR) #添加环境变量
from conf import setting
from src.class_school import School

class Teacher_view(object):
    def __init__(self):
        if os.path.exists(setting.school_file+ '.dat'):
            self.school_file = shelve.open(setting.school_file)
            self.teacher_manger()
            self.school_file.close()
        else:
            print('没有教师数据,请先创建学校')
            sys.exit()
    def teacher_manger(self):
        while True:
            print('欢迎进入IT学院讲师视图:')
            for school_name in self.school_file:
                print('讲师分校名:%s' % school_name)
            school_option = input('请输入您所在分校名>>>:').strip()
            if school_option in self.school_file:
                self.school_option = school_option
                self.school_obj = self.school_file[school_option]
            else:
                print('您的输入有误')
                break
            teacher_option = input('请输入讲师姓名进行管理>>>:').strip()
            if teacher_option in self.school_obj.sch_teacher:
                self.teacher_option = teacher_option
                self.teacher_obj = self.school_obj.sch_teacher[self.teacher_option]
                print('欢迎讲师%s进入讲师管理系统以下是您的讲师信息:'
                      '\n讲师姓名:%s\t讲师年龄:%s\t讲师性别:%s\t讲师工资:%s'
                      %(self.teacher_obj.teacher_name,self.teacher_obj.teacher_name
                        ,self.teacher_obj.teacher_age,self.teacher_obj.teacher_gender,self.teacher_obj.teacher_salary))
            else:
                print('没有[%s]这位讲师'%teacher_option)
                sys.exit()
            while True:
                menu = '''
                          欢迎来到  Python[%s]校区[%s]讲师
                          选择教室  management_class
                          查看班级  view_class
                          查看学员  view_student_list
                          修改成绩  revise_student_grades
                          退出      exit
                          ''' %(school_option,teacher_option)
                print(menu)
                user_choice = input('请选择以上操作>>>:').strip()
                if hasattr(self, user_choice):
                    getattr(self, user_choice)()
                else:
                    print("没有这个操作,请重新输入!!!!")
                    pass

    '''管理自己的班级'''
    def management_class(self):
        for classroom in self.teacher_obj.teacher_classroom:
            class_obj = self.teacher_obj.teacher_classroom[classroom] #教室对象
        print('%s您所在的班级为:%s\t教授的课程是%s:' % (self.teacher_obj.teacher_name,
                                                  class_obj.class_name,class_obj.course_obj.course_name))  # 讲师对应教室和课程
        user_choice = input('是否选择要上课的教室y/n>>>:').strip()
        if user_choice  == 'y':
            class_name = input('请输入要上课的教室>>>:').strip()
            class_obj = self.school_obj.sch_class_room[class_name]
            self.school_obj.create_teacher(self.teacher_obj.teacher_name, self.teacher_obj.teacher_age,
                                           self.teacher_obj.teacher_gender,self.teacher_obj.teacher_salary,class_name,
                                           class_obj)
            print('讲师选择教室对应的课程成功')
            self.school_file.update({self.school_option:self.school_obj})
            self.school_file.close()
        elif user_choice  == 'n':
            print('不对班级进行管理....请重新选择您的操作!!!>>>:')
            pass
        else:
            print('输入不正确')
            pass

    '''上课选择班级和管理班级'''
    def view_class(self):  # 上课选择班级,
        for classroom in self.teacher_obj.teacher_classroom:
            class_obj = self.teacher_obj.teacher_classroom[classroom]  # 教室对象
        print('%s您所在的班级为:%s\t教授的课程是%s:' % (self.teacher_obj.teacher_name,
                                                  class_obj.class_name, class_obj.course_obj.course_name))  # 讲师对应教室和课程

    '''查看学员列表'''
    def view_student_list(self):  # 查看学员列表
        for classroom in self.teacher_obj.teacher_classroom:
            class_obj = self.teacher_obj.teacher_classroom[classroom]  # 教室对象
            stu_list = []
            for j in class_obj.class_student:
                stu_list.append(j)
            print('%s您所在的班级为:%s\t教授的课程是%s\t您班级里的学生有%s:' % (self.teacher_obj.teacher_name,
                                                  class_obj.class_name, class_obj.course_obj.course_name,
                                                  stu_list))  # 讲师对应教室和课程有问题
    '''修改成绩'''
    def revise_student_grades(self):
        self.view_student_list()
        for classroom in self.teacher_obj.teacher_classroom:
            class_obj = self.school_obj.sch_class_room[classroom]  # 教室对象
            student_name = input('请讲师修改成绩的学生的姓名>>>:').strip()
            if student_name in class_obj.class_student:
                student_obj = class_obj.class_student[student_name]
                print('%s童鞋成绩为%s\t课程:%s\t教室:%s'
                        %(student_name, student_obj.student_score, class_obj.course_obj.course_name, class_obj.class_name))
                student_gender = student_obj.student_gender
                student_age = student_obj.student_age
                new_score = input('请讲师修改成绩>>>:').strip()
                self.school_obj.create_student\
                    (student_name, student_gender, student_age, new_score,class_obj.class_name)
                self.school_file.update({self.school_option: self.school_obj})
                self.school_file.close()
                print('%s童鞋修改成功,他的成绩为%s,他的课程是%s,教室为%s'
                      % (student_name, new_score, class_obj.class_name, class_obj.course_obj.course_name))
            else:
                print('没有这个童鞋>>>>>!!!!')

    def exit(self):
        sys.exit('[%s]讲师感谢使用再见'%self.teacher_obj.teacher_name)
