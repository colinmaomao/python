#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Colin Yao
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
#添加环境变量
from core import manage
if __name__ == '__main__':
   manage.center()
