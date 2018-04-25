#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Time:2017/12/19 20:37
__Author__ = 'Sean Yao'
from modules import views
actions = {
    'syncdb': views.syncdb,  # 创建数据库表
    'teacher': views.teacher,  # 进行程序交互
    'student': views.student,  # 创建组
    # 'create_hosts': views.create_hosts,  # 创建主机
    # 'create_bindhosts': views.create_bindhosts,  # 创建绑定关系
    # 'create_remoteusers': views.create_remoteusers,  # 创建远程用户
    # 'view_user_record': views.user_record_cmd  # 查看用户操作命令
}