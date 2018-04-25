#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Time:2017/12/15 21:34
__Author__ = 'Sean Yao'
import sqlalchemy.exc
from modules import models
from conf import settings
from modules.utils import print_err, yaml_parser
from modules.db_conn import engine, session
import codecs

def syncdb(argvs):
    '''
    创建表结构方法
    :param argvs:
    :return:
    '''
    print("Syncing DB....")
    engine = models.create_engine(settings.ConnParams, echo=True)
    models.Base.metadata.create_all(engine)  # 创建所有表结构

def auth_teacher():
    '''
    用户验证
    do the user login authentication
    :return:
    '''
    count = 0
    while count < 3:
        username = input("\033[32;1mUsername:\033[0m").strip()
        if len(username) == 0:
            continue
        password = input("\033[32;1mPassword:\033[0m").strip()
        if len(password) == 0:
            continue
        user_obj = session.query(models.Teacher).filter(models.Teacher.username == username,
                                                        models.Teacher.password == password).first()
        if user_obj:
            return user_obj
        else:
            print("wrong username or password, you have %s more chances." % (3-count-1))
            count += 1
    else:
        print_err("too many attempts.")

def auth_student():
    '''
    用户验证
    do the user login authentication
    :return:
    '''
    count = 0
    while count < 3:
        username = input("\033[32;1mUsername:\033[0m").strip()
        if len(username) == 0:
            continue
        password = input("\033[32;1mPassword:\033[0m").strip()
        if len(password) == 0:
            continue
        user_obj = session.query(models.Student).filter(models.Student.username == username,
                                                        models.Student.password == password).first()
        if user_obj:
            return user_obj
        else:
            print("wrong username or password, you have %s more chances." % (3-count-1))
            count += 1
    else:
        print_err("too many attempts.")

def list1(dict: dict):
    ''' 将字典转化为列表 '''
    keys = dict.keys()
    vals = dict.values()
    list = [(key, val) for key, val in zip(keys, vals)]
    return list

def welcome_msg(user):
    '''
    :param user:
    :return:
    '''
    WELCOME_MSG = '''\033[32;1m
    ------------- Welcome [%s] login  -------------
    \033[0m''' % user.username
    print(WELCOME_MSG)

def show_class(user):
    '''
    show教室
    :param user:
    :return:
    '''
    print('%s 请参照现有课程教室管理' % user.username)
    data = session.query(models.ClassRoom).filter_by().all()
    print('所有班级')
    for index, x in enumerate(data):
        print(index, x.classname)

def show_course(user):
    '''
    展示课程,课程安排,教室
    :param user:
    :return:
    '''
    print('你可以创建班级关系或给学生分配班级')
    teacher_class_obj = session.query(models.TeacherClass).filter_by(teacher_id=user.id).all()
    for i in teacher_class_obj:
        course_teacher_obj = session.query(models.TeacheCourse).filter_by(bind_teacher_class_id=i.id).all()
        for x in course_teacher_obj:
            time_course_obj = session.query(models.CourseClassRecord).filter_by(id=x.bind_course_time_id).first()
            print('课堂ID: %s 课程:%s 课程安排:%s 教室:%s' % (x.id, time_course_obj.course.coursename,
                                                    time_course_obj.course_time.course_time_name,
                                                    i.class_room.classname))

def show_student_class(user):
    print('%s 你所在的班级' % user.username)
    student_class_obj = session.query(models.StudentTeachClass).filter_by(student_qq=user.qq_number).all()
    for i in student_class_obj:
        class_teacher_obj = session.query(models.TeacherClass).filter_by(
            id=i.teacher_course.bind_teacher_class_id).first()
        course_obj = session.query(models.CourseClassRecord).filter_by(
            id=i.teacher_course.bind_course_time_id).first()
        studentname_obj = session.query(models.Student).filter_by(
            qq_number=i.student.qq_number).first()
        print('绑定id:%s 课程:%s 课程时间:%s 讲师:%s 教室:%s 学生名:%s 学生qq %s' % (
            i.id, course_obj.course.coursename, course_obj.course_time.course_time_name,
            class_teacher_obj.teacher.username, class_teacher_obj.class_room.classname,
            studentname_obj.username, studentname_obj.qq_number))

def view_student():
    '''
    查看学生
    '''
    student_obj = session.query(models.Student).filter_by().all()
    for i in student_obj:
        # 学生姓名QQ
        print('现有学生:%s 学生QQ:%s' % (i.username, i.qq_number))
    print("----------- END -----------")

def view_student_class(user):
    '''
    查看该教室的学生,通过学生和老师id反查
    :param user:
    :return:
    '''
    teacher_class_obj = session.query(models.TeacherClass).filter_by(teacher_id=user.id).all()
    for i in teacher_class_obj:
        teachecourse_obj = session.query(
            models.TeacheCourse).filter_by(bind_teacher_class_id=i.id).all()
        for y in teachecourse_obj:
            student_teachclass_obj = session.query(models.StudentTeachClass).filter_by(teacher_course_id=y.id).all()
            for x in student_teachclass_obj:
                class_teacher_obj = session.query(models.TeacherClass).filter_by(
                    id=x.teacher_course.bind_teacher_class_id).first()
                course_obj = session.query(models.CourseClassRecord).filter_by(
                    id=x.teacher_course.bind_course_time_id).first()
                studentname_obj = session.query(models.Student).filter_by(
                    qq_number=x.student.qq_number).first()
                print('绑定id:%s 课程:%s 课程时间:%s 讲师:%s 教室:%s 学生名:%s 学生qq %s' % (
                    x.id, course_obj.course.coursename, course_obj.course_time.course_time_name,
                    class_teacher_obj.teacher.username, class_teacher_obj.class_room.classname,
                    studentname_obj.username, studentname_obj.qq_number))

def view_record(user):
    '''
    查看上课记录
    :param user:
    :return:
    '''
    record_student = session.query(models.RecordStudent).filter_by().all()
    for i in record_student:
        student_teachclass_obj = session.query(models.StudentTeachClass). \
            filter_by(id=i.student_teach_class_id).first()
        class_teacher_obj = session.query(models.TeacherClass).filter_by(
            id=student_teachclass_obj.teacher_course.bind_teacher_class_id).first()
        course_obj = session.query(models.CourseClassRecord).filter_by(
            id=student_teachclass_obj.teacher_course.bind_course_time_id).first()
        studentname_obj = session.query(models.Student).filter_by(
            qq_number=student_teachclass_obj.student.qq_number).first()
        if class_teacher_obj.teacher.username == user.username:
            print('绑定id:%s 课程:%s 课程时间:%s 讲师:%s 教室:%s 学生名:%s 学生qq %s 上课记录:%s' % (
                student_teachclass_obj.id, course_obj.course.coursename, course_obj.course_time.course_time_name,
                class_teacher_obj.teacher.username, class_teacher_obj.class_room.classname,
                studentname_obj.username, studentname_obj.qq_number, i.record.record))

def view_homework(user):
    '''
    查看作业
    :param user:
    :return:
    '''
    record_student = session.query(models.RecordStudent).filter_by().all()
    for i in record_student:
        student_teachclass_obj = session.query(models.StudentTeachClass). \
            filter_by(id=i.student_teach_class_id).first()
        class_teacher_obj = session.query(models.TeacherClass).filter_by(
            id=student_teachclass_obj.teacher_course.bind_teacher_class_id).first()
        course_obj = session.query(models.CourseClassRecord).filter_by(
            id=student_teachclass_obj.teacher_course.bind_course_time_id).first()
        studentname_obj = session.query(models.Student).filter_by(
            qq_number=student_teachclass_obj.student.qq_number).first()
        studenthomework_obj = session.query(models.StudentHomework).filter_by(
            student_teach_class_id=i.student_teach_class_id).first()
        if studenthomework_obj:
            if class_teacher_obj.teacher.username == user.username:
                print('绑定ID %s 课程:%s 课程时间:%s 讲师:%s 教室:%s 学生名:%s 学生qq %s 上课记录:%s 作业:%s' % (
                    student_teachclass_obj.id, course_obj.course.coursename, course_obj.course_time.course_time_name,
                    class_teacher_obj.teacher.username, class_teacher_obj.class_room.classname,
                    studentname_obj.username, studentname_obj.qq_number, i.record.record,
                    studenthomework_obj.homework.home_work))

def view_score(user):
    '''
    查看分数
    :param user:
    :return:
    '''
    record_student = session.query(models.RecordStudent).filter_by().all()
    for i in record_student:
        student_teachclass_obj = session.query(models.StudentTeachClass). \
            filter_by(id=i.student_teach_class_id).first()
        class_teacher_obj = session.query(models.TeacherClass).filter_by(
            id=student_teachclass_obj.teacher_course.bind_teacher_class_id).first()
        course_obj = session.query(models.CourseClassRecord).filter_by(
            id=student_teachclass_obj.teacher_course.bind_course_time_id).first()
        studentname_obj = session.query(models.Student).filter_by(
            qq_number=student_teachclass_obj.student.qq_number).first()
        studenthomework_obj = session.query(models.StudentHomework).filter_by(
            student_teach_class_id=i.student_teach_class_id).first()
        score_obj = session.query(models.RecordScore).filter_by(student_teach_class_id=i.student_teach_class_id).first()
        if studenthomework_obj:
            if score_obj:
                if class_teacher_obj.teacher.username == user.username:
                    if score_obj.student_teacher_class.student.qq_number == studentname_obj.qq_number:
                        print('绑定ID %s 课程:%s 课程时间:%s 讲师:%s 教室:%s 学生名:%s 学生qq %s 上课记录:%s 作业:%s 分数:%s'
                              % (student_teachclass_obj.id, course_obj.course.coursename,
                                 course_obj.course_time.course_time_name, class_teacher_obj.teacher.username,
                                 class_teacher_obj.class_room.classname, studentname_obj.username,
                                 studentname_obj.qq_number, i.record.record, studenthomework_obj.homework.home_work,
                                 score_obj.score.score))

def teacher(argvs):
    '''
    讲师视图
    :param argvs:
    :return:
    '''
    user = auth_teacher()
    if user:
        welcome_msg(user)
        exit_flag = False
        while not exit_flag:
            show_class(user)
            show_course(user)
            msg = '''
            1) 创建班级
            2）添加学员到班级
            3）上课记录
            4）批改成绩
            5）添加学员
            '''
            print(msg)
            while not exit_flag:
                user_option = input("[ (q)quit, select num to manage]:").strip()
                if len(user_option) == 0:
                    continue
                if user_option == 'q':
                    exit_flag = True
                if user_option == '1':
                    course_name = input('请输入班级上的课程>>>>: ')
                    if len(course_name) == 0:
                        print('sorry...班级不能为空')
                        break
                    else:
                        course_time = input('请输入课程时间安排>>>>:')
                        if len(course_time) == 0:
                            print('sorry...课程时间不能为空')
                            break
                        else:
                            class_name = input('请输入班级名称>>>:')
                            if len(class_name) == 0:
                                print('sorry...班级名称不能为空')
                                break
                    # 课程名
                    course_name_obj = session.query(models.Course).filter_by(coursename=course_name).first()
                    # 课程安排
                    course_time_obj = session.query(models.CourseTime).filter_by(course_time_name=course_time).first()
                    # 教室名
                    class_name_obj = session.query(models.ClassRoom).filter_by(classname=class_name).first()
                    # 添加课程
                    if course_name_obj:
                        pass
                    else:
                        course_name_db_obj = models.Course(coursename=course_name)
                        session.add(course_name_db_obj)
                        session.commit()
                    # 添加课程安排
                    if course_time_obj:
                        pass
                    else:
                        course_time_db_obj = models.CourseTime(course_time_name=course_time)
                        session.add(course_time_db_obj)
                        session.commit()
                    if class_name_obj:
                        pass
                    else:
                        class_name_db_obj = models.ClassRoom(classname=class_name)
                        session.add(class_name_db_obj)
                        session.commit()

                    course_name = session.query(models.Course).filter_by(coursename=course_name).first()
                    course_time = session.query(models.CourseTime).filter_by(course_time_name=course_time).first()
                    class_name = session.query(models.ClassRoom).filter_by(classname=class_name).first()

                    # 创建课程课程时间关联
                    course_class_record_id_obj = session.query(models.CourseClassRecord).filter_by(
                        course_id=course_name.id).filter_by(course_time_id=course_time.id).all()
                    if course_class_record_id_obj:
                        pass
                    else:
                        course_class_record_id_obj = models.CourseClassRecord(course_id=course_name.id,
                                                                              course_time_id=course_time.id)
                        session.add(course_class_record_id_obj)
                        session.commit()

                    # 添加讲师教室关联
                    teacher_class_id_obj = session.query(models.TeacherClass).filter_by(
                         teacher_id=user.id).filter_by(class_room_id=class_name.id).all()
                    if teacher_class_id_obj:
                        pass
                    else:
                        teacher_class_id_obj = models.TeacherClass(teacher_id=user.id, class_room_id=class_name.id)
                        session.add(teacher_class_id_obj)
                        session.commit()

                    # 查老师的对象
                    db_teacher_obj = session.query(models.Teacher).filter_by(id=user.id).first()
                    # 查课程对象
                    db_course_name_obj = session.query(models.Course).filter_by(
                        coursename=course_name.coursename).first()
                    # 查课程安排对象
                    db_course_time_obj = session.query(models.CourseTime). \
                        filter_by(course_time_name=course_time.course_time_name).first()
                    # 查教室对象
                    db_class_obj = session.query(models.ClassRoom).filter_by(classname=class_name.classname).first()

                    # 教室讲师关联对象
                    db_teacher_class_obj = session.query(models.TeacherClass).filter_by(
                        class_room_id=db_class_obj.id).filter_by(teacher_id=user.id).first()
                    # 课程课程安排关联对象
                    db_course_class_obj = session.query(models.CourseClassRecord).filter_by(
                        course_id=db_course_name_obj.id).filter_by(course_time_id=db_course_time_obj.id).first()

                    if db_teacher_class_obj and db_course_class_obj:
                        teacher_class = session.query(models.TeacheCourse).filter_by(
                            bind_teacher_class_id=db_teacher_class_obj.id).filter_by(
                            bind_course_time_id=db_course_class_obj.id).all()
                        if teacher_class:
                            print('班级已经关联了')
                        else:
                            teachecourse = models.TeacheCourse(bind_teacher_class_id=db_teacher_class_obj.id,
                                                               bind_course_time_id=db_course_class_obj.id)
                            session.add(teachecourse)
                            session.commit()
                            print('班级创建完毕')
                            show_course(user)

                elif user_option == '2':
                    view_student()
                    view_student_class(user)
                    show_course(user)
                    add_choice = input('[ (y)是,(n)否, select num to manage]:').strip()
                    if add_choice == 'n':
                        break
                    elif add_choice == 'y':
                        teacher_input_qq = input('请输入学员QQ号>>>: ')
                        teacher_input_courseid = input('请输入课堂ID>>>:')
                        try:
                            qq = int(teacher_input_qq)
                            courseid = int(teacher_input_courseid)
                        except ValueError:
                            print('qq或课堂ID必须是数字')
                            break
                        student_teachclass_check_obj = session.query(
                            models.StudentTeachClass).filter_by(
                            teacher_course_id=teacher_input_courseid).filter_by(student_qq=teacher_input_qq).all()
                        if student_teachclass_check_obj:
                            print('学生已经在班级里了....')
                        else:
                            student_obj = session.query(models.Student).filter_by(qq_number=qq).all()
                            if student_obj:
                                for i in student_obj:
                                    if teacher_input_qq == str(i.qq_number):
                                        student_class_obj = models.StudentTeachClass(
                                            teacher_course_id=courseid, student_qq=qq)
                                        session.add(student_class_obj)
                                        session.commit()
                                        view_student_class(user)
                            else:
                                print('没有这个学生')
                    else:
                        print('no this option')

                elif user_option == '3':
                    print('\n%s 管理的班级学员\n' % user.username)
                    view_student_class(user)
                    print('\n%s 管理的班级的上课记录\n' % user.username)
                    view_record(user)
                    record_choice = input('[ (y)是,(n)否, select num to manage]:').strip()
                    if record_choice == 'n':
                        break
                    elif record_choice == 'y':
                        record_id_input = input('请输入绑定id添加学员上课记录:')
                        # 插入绑定关系
                        record_input = input('[ 请输入学员上课记录(y)yes,(no)否]')
                        try:
                            courseid = int(record_id_input)
                        except ValueError:
                            print('绑定ID必须是数字')
                            break
                        if record_input == 'yes' or 'no':
                            record_in_obj = session.query(
                                models.RecordStudent).filter_by(student_teach_class_id=record_id_input).all()
                            if record_in_obj:
                                print('记录已经添加...')
                                break
                            else:
                                record_in_obj = session.query(models.Record).filter_by(record=record_input).first()
                                student_teachclass_id_obj = models.RecordStudent(
                                    student_teach_class_id=record_id_input, record_id=record_in_obj.id)
                                session.add(student_teachclass_id_obj)
                                session.commit()
                                view_record(user)
                    else:
                        print('no this option')
                        break

                elif user_option == '4':
                    print('\n%s 管理的班级的上课记录\n' % user.username)
                    view_record(user)
                    print('\n已交作业的童鞋\n')
                    view_homework(user)
                    print('\n已批改的成绩\n')
                    view_score(user)
                    choice_score_input = input('[ 批改成绩是否继续(y)是,(n)否, select num to manage]:').strip()
                    if choice_score_input == 'n':
                        break
                    elif choice_score_input == 'y':
                        record_id_input = input('请输入显示的绑定id添加学员成绩:')
                        score_input = input('请输入分数..')
                        # 插入绑定关系
                        home_work_check = session.query(
                            models.StudentHomework).filter_by(student_teach_class_id=int(record_id_input)).all()
                        if home_work_check:
                            score = int(score_input)
                            if score > 100 or score < 0:
                                print('请输入100以内的整数')
                            else:
                                score_obj = session.query(models.Score).filter_by(score=score).all()
                                if score_obj:
                                    for i in score_obj:
                                        score_db_id_obj = session.query(
                                            models.Score).filter_by(score=i.score).first()
                                        record_score_obj = session.query(models.RecordScore).filter_by(
                                            student_teach_class_id=record_id_input).first()
                                        if record_score_obj:
                                            print('该学员已经有成绩了...')
                                            break
                                        else:
                                            add_score_obj = models.RecordScore(
                                                student_teach_class_id=record_id_input, score_id=score_db_id_obj.id)
                                            session.add(add_score_obj)
                                            session.commit()
                                            print('添加成绩完成')
                                            view_score(user)
                                else:
                                    score_db_obj = models.Score(score=score)
                                    session.add(score_db_obj)
                                    session.commit()
                                    score_db_id_obj = session.query(models.Score).filter_by(score=score).first()
                                    record_score_obj = session.query(models.RecordScore).filter_by(
                                        student_teach_class_id=record_id_input).first()
                                    if record_score_obj:
                                        print('该学员已经有成绩了...')
                                        break
                                    else:
                                        add_score_obj = models.RecordScore(
                                            student_teach_class_id=record_id_input, score_id=score_db_id_obj.id)
                                        session.add(add_score_obj)
                                        session.commit()
                                        print('添加成绩完成')
                                        view_score(user)
                        else:
                            print('学生还没有交作业,请先联系学生交作业')
                            break
                    else:
                        print('no this option')
                        pass
                elif user_option == '5':
                    print('添加学员后请注意给学生分配教室并添加上课记录，课后请提示学生交作业')
                    student_add_input = input('[ (y)是,(n)否, select num to manage]:').strip()
                    student_name_input = input('请输入学生账号:')
                    student_password_input = input('请输入学生密码:')
                    student_qq_input = input('请输入学生qq号码:')
                    try:
                        qq = int(student_qq_input)
                    except ValueError:
                        print('qq必须是数字')
                        break
                    # 联合查询
                    student_check = session.query(
                        models.Student).filter_by(qq_number=qq).filter_by(username=student_name_input).all()
                    if student_check:
                        print('学生已经存在')
                    else:
                        # 联合查询不能避免qq号或用户名重复...数据库中做了qq号和用户名唯一
                        try:
                            student_obj = models.Student(
                                qq_number=qq, username=student_name_input, password=student_password_input)
                            session.add(student_obj)
                            session.commit()
                            print('添加学生完成,请给学生分配教室课后请添加上课记录并提示学生交作业')
                        except sqlalchemy.exc.IntegrityError:
                            print('学生已经存在')
                elif user_option == 'q':
                    exit_flag = True
                else:
                    print("no this option..")

def student(argvs):
    '''
    学生视图
    :param argvs:
    :return:
    '''
    user = auth_student()
    if user:
        print('student')
        welcome_msg(user)
        exit_flag = False
        show_student_class(user)
        msg = '''
        1）选择课程班级
        2) 提交作业
        3）查看作业成绩
        4）查看所属班级成绩排名
        '''
        print(msg)
        while not exit_flag:
            user_option = input("[ (q)quit, select num to manage]:").strip()
            if len(user_option) == 0:
                continue
            if user_option == 'q':
                exit_flag = True
            if user_option == '1':
                print('请联系您的讲师帮您安排课程和教室')
            elif user_option == '2':
                home_work_add_choice = input('[ (y)是,(n)否, select num to manage]:').strip()
                if home_work_add_choice == 'n':
                    break
                elif home_work_add_choice == 'y':
                    home_work_course_time_input = input('请输入上课节数/课程时间>>>:')
                    home_work_classroom_input = input('请输入所在班级/教室>>>: ')
                    home_work_classid_input = input('请输入对应教室的绑定ID>>>:')
                    student_class_obj = session.query(models.StudentTeachClass).filter_by(
                        id=int(home_work_classid_input)).all()
                    if student_class_obj:
                        for i in student_class_obj:
                            course_obj = session.query(models.CourseClassRecord).filter_by(
                                id=i.teacher_course.bind_course_time_id).first()
                            # 检查作业
                            student_home_work_id_check = session.query(
                                models.HomeWork).filter_by(home_work=user.username+'_'+course_obj.course_time.
                                                           course_time_name+'_'+'home_work').all()
                            if student_home_work_id_check:
                                print('已经交作业了，不需要重复提交')
                            else:
                                home_add = input('[ (y)是,(n)否, to add home_work]:').strip()
                                if home_add == 'n':
                                    break
                                if home_add == 'y':
                                    homework = \
                                        models.HomeWork(
                                            home_work=user.username+'_' + course_obj.course_time.course_time_name + '_' +
                                                      'home_work')
                                    session.add(homework)
                                    session.commit()
                                    home_work_id = session.query(models.HomeWork).filter_by(
                                            home_work=user.username+'_' + course_obj.course_time.course_time_name+'_' +
                                                      'home_work').first()
                                    record_home_work = models.StudentHomework(
                                        student_teach_class_id=i.id, homework_id=home_work_id.id)
                                    session.add(record_home_work)
                                    session.commit()
                                    print('作业添加完成,请提醒老师添加上课记录和批改成绩...')
                                    break
                    else:
                        print('没有这个班级...')

            elif user_option == '3':
                print('如果没有成绩的请先交作业然后找讲师批改成绩')
                student_record_id = input('请输入您的绑定ID，查看作业信息;')
                record_student = session.query(models.RecordStudent).filter_by().all()
                for i in record_student:
                    student_teachclass_obj = session.query(models.StudentTeachClass). \
                        filter_by(id=student_record_id).first()
                    class_teacher_obj = session.query(models.TeacherClass).filter_by(
                        id=student_teachclass_obj.teacher_course.bind_teacher_class_id).first()
                    course_obj = session.query(models.CourseClassRecord).filter_by(
                        id=student_teachclass_obj.teacher_course.bind_course_time_id).first()
                    studentname_obj = session.query(models.Student).filter_by(
                        qq_number=user.qq_number).first()
                    studenthomework_obj = session.query(models.StudentHomework).filter_by(
                        student_teach_class_id=student_record_id).first()
                    score_obj = session.query(models.RecordScore).filter_by(
                        student_teach_class_id=i.student_teach_class_id).first()
                    if studenthomework_obj:
                        if user.username == studentname_obj.username:
                            if score_obj:
                                if score_obj.student_teacher_class.student.qq_number == studentname_obj.qq_number:
                                    print('绑定ID %s 课程:%s 课程时间:%s 讲师:%s 教室:%s 学生名:%s 学生qq %s 上课记录:%s 作业:%s 分数:%s'
                                          % (student_teachclass_obj.id, course_obj.course.coursename,
                                             course_obj.course_time.course_time_name,
                                             class_teacher_obj.teacher.username,
                                             class_teacher_obj.class_room.classname, studentname_obj.username,
                                             studentname_obj.qq_number, i.record.record,
                                             studenthomework_obj.homework.home_work,
                                             score_obj.score.score))

            elif user_option == '4':
                print('查看班级排名.请按照所在班级的绑定ID查询排名')
                home_work_course_time_input = input('请输入上课节数/课程时间>>>:')
                home_work_classroom_input = input('请输入所在班级/教室>>>: ')
                record_student = session.query(models.RecordStudent).filter_by().all()
                tmp_dict = {}
                for i in record_student:
                    student_teachclass_obj = session.query(models.StudentTeachClass). \
                        filter_by(id=i.student_teach_class_id).first()
                    class_teacher_obj = session.query(models.TeacherClass).filter_by(
                        id=student_teachclass_obj.teacher_course.bind_teacher_class_id).first()
                    course_obj = session.query(models.CourseClassRecord).filter_by(
                        id=student_teachclass_obj.teacher_course.bind_course_time_id).first()
                    studentname_obj = session.query(models.Student).filter_by(
                        qq_number=student_teachclass_obj.student.qq_number).first()
                    studenthomework_obj = session.query(models.StudentHomework).filter_by(
                        student_teach_class_id=i.student_teach_class_id).first()
                    score_obj = session.query(models.RecordScore).filter_by(
                        student_teach_class_id=i.student_teach_class_id).first()
                    if home_work_course_time_input == course_obj.course_time.course_time_name \
                            and home_work_classroom_input == class_teacher_obj.class_room.classname:
                        if studenthomework_obj:
                            if score_obj:
                                if score_obj.student_teacher_class.student.qq_number == studentname_obj.qq_number:
                                    if score_obj.score.score in tmp_dict.keys():
                                        tmp_dict[score_obj.score.score].append(studentname_obj.username)
                                    else:
                                        tmp_dict[score_obj.score.score] = [studentname_obj.username]
                # 分数排序,按道理应该是用group_by 这里偷个懒
                tmp_list = []
                for key in tmp_dict.keys():
                    tmp_list.append(key)
                tmp_list.sort(reverse=True)
                for key in tmp_list:
                    for name in tmp_dict[key]:
                        print(name, key)

            elif user_option == 'q':
                exit_flag = True
            else:
                print('no this option')