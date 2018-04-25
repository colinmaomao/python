#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Time:2017/12/15 21:22
__Author__ = 'Sean Yao'
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

if __name__ == '__main__':
    from modules.actions import excute_from_command_line
    excute_from_command_line(sys.argv)