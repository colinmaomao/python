#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Colin Yao
import  os
import sys
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
from core import fortress_main

if __name__ == '__main__':
    fortress_main.fortress_machine().user_choice()

