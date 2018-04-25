#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Time:2017/12/14 19:06
__Author__ = 'Sean Yao'
from sqlalchemy import Table, Column, Integer, String, DATE, ForeignKey, Enum, UniqueConstraint
# uniqueconstraint 联合唯一
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import ChoiceType, PasswordType  # sqlalchemy_utils sqalchemy_utils插件

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

Base = declarative_base()  # 基类

# 多对多关联,BindHost连接remote_user
user_m2m_bindhost = Table('user_m2m_bindhost', Base.metadata,
                          Column('userprofile_id', Integer, ForeignKey('user_profile.id')),
                          Column('bind_host_id', Integer, ForeignKey('bind_host.id')),)

class BindHost(Base):
    '''
    关联关系
    192.168.1.11 web  bj_group
    192.168.1.11 mysql sh_group
    '''
    __tablename_ = "bind_host"
    # 联合唯一
    __table_args__ = (UniqueConstraint('host_id', 'group_id', 'remoteuser_id', name='_host_group_remoteuser_uc'))

    id = Column(Integer, primary_key=True)
    # 外键关联
    host_id = Column(Integer, ForeignKey('host.id'))
    group_id = Column(Integer, ForeignKey('group.id'))
    remoteuser_id = Column(Integer, ForeignKey('remote_user.id'))

    host = relationship('Host', backref='bind_hosts')
    host_group = relationship('HostGroup', backref='bind_hosts')
    remote_user = relationship("RemoteUser", backref='bind_hosts')

    def __repr__(self):
        return "<%s -- %s -- %s>" % (self.host.ip,
                                     self.remote_user.username,
                                     self.host_group.name)

class Host(Base):
    '''
    远程主机
    '''
    __tablename = 'host'
    id = Column(Integer, primary_key=True)
    hostname = Column(String(64), unique=True)
    ip = Column(String(64), unique=True)
    port = Column(Integer, default=22)
    # 不要让主机关联主机组，这样权限给主机组了，应该是将用户密码和主机组绑定，
    # 比如root 123 sh root 123 bj 这样他可以用所有的权限,

    def __repr__(self):
        return self.hostname

class HostGroup(Base):
    '''
    远程主机组
    '''
    __tablename = 'host_group'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)

    def __repr__(self):
        return self.name


class RemoteUser(Base):
    '''
    远程用户密码表
    '''
    __tablename = 'remote_user'
    #  联合唯一
    __table_args__ = (UniqueConstraint('auth_type', 'username', 'password', name='_user_passwd_uc'))
    id = Column(Integer, primary_key=True)
    AuthTypes = [
        ('ssh-password', 'SSH/Password'),  # 第一个是存在数据库里的,第二个具体的值
        ('ssh-key', 'SSH/KEY')
    ]
    auth_type = Column(ChoiceType(AuthTypes))
    username = Column(String(32))
    password = Column(String(128))

    def __repr__(self):
        return self.username

class Userprofile(Base):
    '''
    堡垒机用户表
    '''
    __tablename = 'user_profile'
    id = Column(Integer, primary_key=True)
    username = Column(String(32), unique=True)
    password = Column(String(128))
    bind_hosts = relationship("BindHost", secondary='user_m2m_bindhost', backref='user+profiles')

    def __repr__(self):
        return self.username

class AuditLog(Base):
    '''
    日志信息表
    '''
    pass
