#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Colin Yao
"""模拟计算器开发作业"""
import re
def operator_update(formula):
    formula = formula.replace(" ", "")
    formula = formula.replace("+-", "-")
    formula = formula.replace("--", "+")
    return formula

def calc_muldiv(formula_list):
    for index, element in enumerate(formula_list):
        if "*" in element or "/" in element:
            operators = re.findall("[*/]", element)
            calc_list = re.split("[*/]", element)
            num = None
            for i, e in enumerate(calc_list):
                if num:
                    if operators[i - 1] == "*":
                        num *= float(e)
                    elif operators[i - 1] == "/":
                        num /= float(e)
                else:
                    num = float(e)
            formula_list[index] = num
    return formula_list

def calc_plumin(operators, num_list):
    num = None
    for i, e in enumerate(num_list):
        if num:
            if operators[i - 1] == "+":
                num += float(e)
            elif operators[i - 1] == "-":
                num -= float(e)
        else:
            num = float(e)
    return num

def merge(plus_minus_operator, multiply_divide_list):
    for index, element in enumerate(multiply_divide_list):
        if element.endswith("*") or element.endswith("/"):
            multiply_divide_list[index] = element + plus_minus_operator[index] + multiply_divide_list[index + 1]
            del multiply_divide_list[index + 1]
            del plus_minus_operator[index]
            return merge(plus_minus_operator, multiply_divide_list)
    return plus_minus_operator, multiply_divide_list

def bracket_calc(formula):
    formula = re.sub("[()]", "", formula)  # 去除两边的（）
    formula = operator_update(formula)
    plus_minus_operator = re.findall("[+-]", formula)
    multiply_divide_list = re.split("[+-]", formula)
    if multiply_divide_list[0] == "":
        multiply_divide_list[1] = "-" + multiply_divide_list[1]
        del plus_minus_operator[0]
        del multiply_divide_list[0]
    res = merge(plus_minus_operator, multiply_divide_list)
    plus_minus_operator = res[0]
    multiply_divide_list = res[1]
    plus_minus_list = calc_muldiv(multiply_divide_list)
    res = calc_plumin(plus_minus_operator, plus_minus_list)
    return res

def calculate(formula):
    while True:
        formula_depth = re.search("\([^()]+\)", formula)
        if formula_depth:
            formula_depth = formula_depth.group()
            res = bracket_calc(formula_depth)
            formula = formula.replace(formula_depth, str(res))
            print(formula)
        else:
            res = bracket_calc(formula)
            print(res)
            exit()


if __name__ == '__main__':
    msg = '''
        进行解析()的运算
        例如:1 - 2 * ( (60-30 +(-40/5) * (9-2*5/3 + 7 /3*99/4*2998 +10 * 568/14 )) - (-4*3)/ (16-3*2) )

        '''
    print(msg)
    formula = input("请输入要进行的运算>>>:")
    #  formula = "1 - 2 * ( (60-30 +(-40/5) * (9-2*5/3 + 7 /3*99/4*2998 +10 * 568/14 )) - (-4*3)/ (16-3*2) )"
    calculate(formula)