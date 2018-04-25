#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Colin Yao
import  os,time,shelve,sys
from src.class_school import School
BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR) #添加环境变量
data_path = os.path.join(BASE_DIR+'\db')
school_file = os.path.join(data_path,'school')
