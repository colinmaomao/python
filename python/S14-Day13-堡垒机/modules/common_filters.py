#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Time:2017/12/18 18:19
__Author__ = 'Sean Yao'
from models import models
from modules.db_conn import engine, session
from modules.utils import print_err

def bind_hosts_filter(vals):
    '''

    :param vals:
    :return:
    '''
    print('**>', vals.get('bind_hosts'))
    bind_hosts = session.query(models.BindHost).filter(models.Host.hostname.in_(vals.get('bind_hosts'))).all()
    if not bind_hosts:
        print_err("none of [%s] exist in bind_host table." % vals.get('bind_hosts'), quit=True)
    return bind_hosts

def user_profiles_filter(vals):
    '''

    :param vals:
    :return:
    '''
    user_profiles = session.query(models.Userprofile).filter(models.Userprofile.username.in_(vals.get('user_profiles'))
                                                             ).all()
    if not user_profiles:
        print_err("none of [%s] exist in user_profile table." % vals.get('user_profiles'), quit=True)
    return user_profiles
