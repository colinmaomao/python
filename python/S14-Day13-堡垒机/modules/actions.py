#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Time:2017/12/15 21:31
__Author__ = 'Sean Yao'

from conf import action_registers
from modules import utils


def help_msg():
    '''
    print help msgs
    :return:
    '''
    print("\033[31;1mAvailable commands:\033[0m")
    for key in action_registers.actions:
        print("\t", key)

def excute_from_command_line(argvs):
    '''
    print
    :param argvs:
    :return:
    '''
    if len(argvs) < 2:
        help_msg()
        exit()
    if argvs[1] not in action_registers.actions:
        utils.print_err("Command [%s] does not exist!" % argvs[1], quit=True)
        # utils 工具箱
    action_registers.actions[argvs[1]](argvs[1:])
