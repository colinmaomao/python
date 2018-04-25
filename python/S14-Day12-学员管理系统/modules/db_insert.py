#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Time:2017/12/20 12:25
__Author__ = 'Sean Yao'
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from modules import models

engine = create_engine("mysql+pymysql://root:123456@192.168.84.66/managedb?charset=utf8",
                       encoding='utf-8')  # ,echo=True)

Base = declarative_base()
Session_class = sessionmaker(bind=engine)
Session = Session_class()

# 创建课程
user_obj = models.Course(coursename='python')  # 生成你要创建的数据对象
user_obj2 = models.Course(coursename='linux')  # 生成你要创建的数据对象
Session.add(user_obj)
Session.add(user_obj2)
Session.commit()

# 创建课程表
user_obj = models.CourseTime(course_time_name='python_day1')  # 生成你要创建的数据对象
user_obj2 = models.CourseTime(course_time_name='linux_day1')  # 生成你要创建的数据对象
Session.add(user_obj)
Session.add(user_obj2)
Session.commit()

# 创建讲师
user_obj = models.Teacher(username='alex', password='123456')  # 生成你要创建的数据对象
user_obj2 = models.Teacher(username='alexli', password='123456')  # 生成你要创建的数据对象
Session.add(user_obj)
Session.add(user_obj2)
Session.commit()

# 创建教室
user_obj = models.ClassRoom(classname='python1')  # 生成你要创建的数据对象
user_obj2 = models.ClassRoom(classname='linux1')  # 生成你要创建的数据对象
Session.add(user_obj)
Session.add(user_obj2)
Session.commit()
#
# 创建学生
user_obj = models.Student(qq_number='449010391', username='colin', password='123')  # 生成你要创建的数据对象
user_obj2 = models.Student(qq_number='449010392', username='sean', password='1234')  # 生成你要创建的数据对象
Session.add(user_obj)
Session.add(user_obj2)
Session.commit()

# 创建成绩
user_obj = models.Score(score=66)  # 生成你要创建的数据对象
user_obj2 = models.Score(score=77)
Session.add(user_obj)
Session.add(user_obj2)
Session.commit()

# 创建作业
user_obj = models.HomeWork(home_work='colin_homework')  # 生成你要创建的数据对象
user_obj2 = models.HomeWork(home_work='sean_homework')  # 生成你要创建的数据对象
Session.add(user_obj)
Session.add(user_obj2)
Session.commit()

# 创建记录
user_obj = models.Record(record='no')  # 生成你要创建的数据对象
user_obj2 = models.Record(record='yes')   # 生成你要创建的数据对象
Session.add(user_obj)
Session.add(user_obj2)
Session.commit()
#
# 创建课程课程时间关联
user_obj = models.CourseClassRecord(course_id=1, course_time_id=1)  # 生成你要创建的数据对象
user_obj2 = models.CourseClassRecord(course_id=2, course_time_id=2)  # 生成你要创建的数据对象
Session.add(user_obj)
Session.add(user_obj2)
Session.commit()
# #
# 创建老师班级关联
user_obj = models.TeacherClass(teacher_id=1, class_room_id=1)  # 生成你要创建的数据对象
user_obj2 = models.TeacherClass(teacher_id=2, class_room_id=2)  # 生成你要创建的数据对象
Session.add(user_obj)
Session.add(user_obj2)
Session.commit()

# 课程/课程表/讲师/教室关联
user_obj = models.TeacheCourse(bind_teacher_class_id=1, bind_course_time_id=1)  # 生成你要创建的数据对象
user_obj2 = models.TeacheCourse(bind_teacher_class_id=2, bind_course_time_id=2)
Session.add(user_obj)
Session.add(user_obj2)
Session.commit()

# 学生/ 课程/课程表/讲师/教室关联
user_obj = models.StudentTeachClass(teacher_course_id=1, student_qq=449010391)  # 生成你要创建的数据对象
user_obj2 = models.StudentTeachClass(teacher_course_id=2, student_qq=449010392)
Session.add(user_obj)
Session.add(user_obj2)
Session.commit()

# 课程/课程表/讲师/教室/学生/作业/关联 学生视图操作
user_obj = models.StudentHomework(student_teach_class_id=1, homework_id=1)  # 生成你要创建的数据对象
user_obj2 = models.StudentHomework(student_teach_class_id=2, homework_id=2)
Session.add(user_obj)
Session.add(user_obj2)
Session.commit()
# 课程/课程表/讲师/教室/学生/上课记录关联 讲师视图操作
user_obj = models.RecordStudent(student_teach_class_id=1, record_id=1)  # 生成你要创建的数据对象
user_obj2 = models.RecordStudent(student_teach_class_id=2, record_id=2)
Session.add(user_obj)
Session.add(user_obj2)
Session.commit()

#  课程/课程表/讲师/教室/学生/成绩关联
user_obj = models.RecordScore(student_teach_class_id=1, score_id=1)  # 生成你要创建的数据对象
user_obj2 = models.RecordScore(student_teach_class_id=2, score_id=2)
Session.add(user_obj)
Session.add(user_obj2)
Session.commit()

data = Session.query(models.StudentTeachClass).filter_by().all()
for i in data:
    id = i.id
    x = Session.query(models.Student).filter_by(qq_number=i.student.qq_number).first()
    x1 = Session.query(models.TeacherClass).filter_by(id=i.teacher_course.bind_teacher_class_id).first()
    x2 = Session.query(models.CourseClassRecord).filter_by(id=i.teacher_course.bind_course_time_id).first()
    x3 = Session.query(models.RecordScore).filter_by(id=id).first()
    x4 = Session.query(models.RecordStudent).filter_by(id=id).first()
    x5 = Session.query(models.StudentHomework).filter_by(id=id).first()
    # print(x3.record.record, x3.homework.home_work, x3.score.score)
    print('课程名称:', x2.course.coursename, '课程时间:', x2.course_time.course_time_name,
          '讲师名称：', x1.teacher.username, '所在班级:', x1.class_room.classname, '学员名称:', i.student.username,
          '上课记录:', x4.record.record, '作业:', x5.homework.home_work, '得分', x3.score.score)