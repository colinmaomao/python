#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Time:2017/12/19 20:36
__Author__ = 'Sean Yao'
import datetime
from sqlalchemy import Table, Column, Integer, String, DATE, ForeignKey, Enum, UniqueConstraint, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import ChoiceType, PasswordType
from sqlalchemy import create_engine

Base = declarative_base()

class TeacheCourse(Base):
    '''
    课程/课程表/讲师/教室/关联
    '''
    __tablename__ = 'teacher_course'
    __table_args__ = (UniqueConstraint('bind_teacher_class_id', 'bind_course_time_id', name='_class_uc'),)
    id = Column(Integer, primary_key=True)
    bind_teacher_class_id = Column('bind_teacher_class_id', Integer, ForeignKey('bind_teacher_class.id'))
    bind_course_time_id = Column('bind_course_time_id', Integer, ForeignKey('bind_course_time.id'))

    teacher_class = relationship('TeacherClass', backref='teacher_course')
    course_class_record = relationship('CourseClassRecord', backref='teacher_course')

    def __repr__(self):
        return self.id, self.teacher_class.id, self.bind_course_time_id


class RecordScore(Base):
    '''
    打分/关联 老师视图操作
   1  66
   2  88
    '''
    __tablename__ = 'record_score'
    __table_args__ = (UniqueConstraint('student_teach_class_id', 'score_id', name='_record_score_uc'),)

    id = Column(Integer, primary_key=True)
    student_teach_class_id = Column(
        'student_teach_class_id', Integer, ForeignKey('student_teach_class.id'), unique=True)
    score_id = Column('score_id', Integer, ForeignKey('score.id'))

    score = relationship('Score', backref='record_score')
    student_teacher_class = relationship('StudentTeachClass', backref='record_score')

    def __repr__(self):
        return self.id, self.student_teacher_class.teacher_course.id, self.student_teacher_class.student.qq_number, \
               self.score.score

class RecordStudent(Base):
    '''
    上课记录/关联 老师视图操作
   1  yes
   2  no
    '''
    __tablename__ = 'record_student'
    __table_args__ = (UniqueConstraint('student_teach_class_id', 'record_id', name='_record_class_uc'),)

    id = Column(Integer, primary_key=True)
    student_teach_class_id = Column(
        'student_teach_class_id', Integer, ForeignKey('student_teach_class.id'), unique=True)
    record_id = Column('record_id', Integer, ForeignKey('record.id'))

    record = relationship('Record', backref='record_student')
    student_teacher_class = relationship('StudentTeachClass', backref='record_student')

    def __repr__(self):
        return self.id, self.student_teacher_class.teacher_course.id, self.student_teacher_class.student.qq_number, \
               self.record.record

class StudentHomework(Base):
    '''
    课程/课程表/讲师/教室/学生/作业/关联 学生视图操作
    449010391 1
    '''
    __tablename__ = 'student_homework'
    __table_args__ = (UniqueConstraint('student_teach_class_id', 'homework_id', name='_record_homework_uc'),)

    id = Column(Integer, primary_key=True)
    student_teach_class_id = Column(
        'student_teach_class_id', Integer, ForeignKey('student_teach_class.id'), unique=True)
    homework_id = Column('homework_id', Integer, ForeignKey('homework.id'))

    homework = relationship('HomeWork', backref='student_homework')
    student_teacher_class = relationship('StudentTeachClass', backref='student_homework')

    def __repr__(self):
        return self.id, self.student_teacher_class.teacher_course.id, self.student_teacher_class.student.qq_number, \
               self.homework.home_work

class StudentTeachClass(Base):
    '''
    课程/课程表/讲师/教室/学生/关联
    python/python1/alex/python_1  449010391
                  1               449010391
    '''
    __tablename__ = 'student_teach_class'
    __table_args__ = (UniqueConstraint('student_qq', 'teacher_course_id', name='_record_uc'),)

    id = Column(Integer, primary_key=True)
    teacher_course_id = Column('teacher_course_id', Integer, ForeignKey('teacher_course.id'))
    student_qq = Column('student_qq', Integer, ForeignKey('student.qq_number'))

    teacher_course = relationship("TeacheCourse", backref='student_teach_class')
    student = relationship('Student', backref='student_teach_class')

    def __repr__(self):
        # qq号,讲师/教室/课程/课程表
        return self.id, self.student.qq_number, self.teacher_course.bind_teacher_class_id, \
               self.teacher_course.bind_course_time_id

class Course(Base):
    '''
    课程表
    课程唯一
    '''
    __tablename__ = 'course'
    id = Column(Integer, primary_key=True)
    coursename = Column(String(64), unique=True, nullable=False)

    def __repr__(self):
        return self.id, self.coursename

class CourseTime(Base):
    '''
    课程时间表
    课程时间唯一
    '''
    __tablename__ = 'course_time'
    id = Column(Integer, primary_key=True)
    course_time_name = Column(String(64), unique=True, nullable=False)

    def __repr__(self):
        return self.id, self.course_time_name

class Teacher(Base):
    '''
    teacher 表
    老师名字唯一
    '''
    __tablename__ = 'teacher'
    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, nullable=False)
    password = Column(String(128), nullable=False)

    def __repr__(self):
        return self.id, self.username, self.password,

class ClassRoom(Base):
    '''
    班级表
    班级唯一
    '''
    __tablename__ = 'class_room'
    id = Column(Integer, primary_key=True)
    classname = Column(String(64), unique=True, nullable=False)

    def __repr__(self):
        return self.id, self.classname

class Student(Base):
    '''
    student表
    用户名/qq号/唯一
    '''
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True)
    qq_number = Column(Integer, unique=True, nullable=False)
    username = Column(String(64), unique=True, nullable=False)
    password = Column(String(128), nullable=False)

    def __repr__(self):
        return self.id, self.qq_number, self.username, self.password

class Score(Base):
    '''
    成绩表
    成绩不唯一可能不同的童鞋得到的分数一样
    '''
    __tablename__ = 'score'
    id = Column(Integer, primary_key=True)
    score = Column(Integer, unique=True, nullable=False)

    def __repr__(self):
        return self.id, self.score

class HomeWork(Base):
    '''
    作业表
    作业唯一对应不同的童鞋和课程
    '''
    __tablename__ = 'homework'
    id = Column(Integer, unique=True, primary_key=True)
    home_work = Column(String(128))

    def __repr__(self):
        return self.id, self.home_work

class Record(Base):
    '''
    上课记录
    唯一只有yes/no
    '''
    __tablename__ = 'record'
    id = Column(Integer, primary_key=True)
    action_choices = [
        (u'yes', u'Yes'),
        (u'no', u'No'),
    ]
    record = Column(ChoiceType(action_choices), unique=True)

    def __repr__(self):
        return self.id, self.record

class CourseClassRecord(Base):
    '''
    课程/课程时间/关联
    课程:pyrhon  课程时间:python_day1
    课程:linux 课程时间:linux_day1
    课程:linux 课程时间:linux_day2
    课程和课程时间联合唯一
    '''
    __tablename__ = "bind_course_time"
    # 联合唯一
    __table_args__ = (UniqueConstraint('course_id', 'course_time_id', name='_course_uc'),)
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('course.id'))
    course_time_id = Column(Integer, ForeignKey('course_time.id'))
    course = relationship('Course', backref='bind_course_time')
    course_time = relationship('CourseTime', backref='bind_course_time')

    def __repr__(self):
        return self.id, self.course.coursename, self.course_time.course_time_name

class TeacherClass(Base):
    '''
    老师/班级/关联
    老师和班级联合唯一
    老师:alex  班级:python_S14
    老师:alex  班级:python_S15
    '''
    __tablename__ = "bind_teacher_class"
    __table_args__ = (UniqueConstraint('teacher_id', 'class_room_id', name='_class_uc'),)

    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer, ForeignKey('teacher.id'))
    class_room_id = Column(Integer, ForeignKey('class_room.id'))
    teacher = relationship('Teacher', backref='bind_teacher_class')
    class_room = relationship('ClassRoom', backref='bind_teacher_class')

    def __repr__(self):
        return self.id, self.teacher.username, self.class_room.classname