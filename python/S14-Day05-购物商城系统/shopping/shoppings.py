# -*- coding: utf-8 -*-
import pickle,os,sys,json
BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR) #添加环境变量
_db_shopping_record = BASE_DIR + r"\db\accounts\shopping_db"
_db_shopping_cache = BASE_DIR + r"\db\accounts\shopping_cache"
from core import auth,creditcard
from conf import settings

product_list = [
        ('Iphone 6s', 5299),
        ('Iphone 6s Plus', 5999),
        ('Sumsung s7', 3888),
        ('Sumsung s7 Edge', 5688),
        ('360 F4 ', 799),
        ('红米Note3 ', 899),
        ('魅族 MX6', 1999),
        ('华为 Mate', 2799),
    ]


f = open(_db_shopping_record, 'rb')
user_list = pickle.load(f)
f.close()

def wirte_logout():
    f = open(_db_shopping_record, 'wb')
    pickle.dump(user_list, f)
    f.close()
    return

def index_page():
    page = '''

[0]登录 [1]注册 [2]浏览

'''
    print('\n', '手机商城测试页面'.center(60, '-'),page)
    return


def login():
    print('\n')
    global user
    count = 1
    for i in range(5):
        if count <= 3:
            user = input('用户登录： ')
            password = input('密 码： ')
            if user in user_list.keys():
                if user == user_list[user]['username'] and password == user_list[user]['userpasswd']:
                    print("欢迎%s光临"%user)
                    return user
                    print(msg)
                    break
                else:
                    print('用户名或密码不正确,请重新登录！')
            else:
                user_choice = input('用户不存在,是否需要注册(y/n)')
                if user_choice == 'y':
                    add_user()
                    break
                elif user_choice == 'n':
                    pass
            count += 1
        elif count > 3:
            exit('超出登录次数！登录失败')
    return


def add_user():
    global user
    exit_flag = False
    print('\n')
    while not exit_flag:
        username = input('请输入你的用户名：')
        if username in user_list.keys():
            print('\n用户名已存在，请输入其他名称\n')
        else:
            exit_flag = True
    userpasswd = input('请输入你的密码')
    user_list[username] = {}
    user_list[username]['username'] = username
    user_list[username]['userpasswd'] = userpasswd
    user_list[username]['salary'] = ''
    user_list[username]['shop_car'] = ''
    user_list[username]['shop_car_list'] = ''
    print('\n注册成功，你的用户名是：%s' % username, '\n')
    user = user_list[username]['username']
    wirte_logout()
    return


def print_product_list():
    print('\n产品列表:\n')
    for item in enumerate(product_list):
        index = item[0]
        p_name = item[1][0]
        p_price = item[1][1]
        print(index, ':', p_name, p_price)
    return


def printending():
    print('购物车中的商品'.center(50, '-'))
    for item in user_list[user]['shop_car']:
        a = user_list[user]['shop_car'].index(item)
        print('商品:%s  价格:%s  数量:%s' % (
        user_list[user]['shop_car'][a][0], user_list[user]['shop_car'][a][1], user_list[user]['shop_car_list'][a]))
    print('End'.center(50, '-'))
    return


"""调用信用卡auth 登陆 信用卡接口进行结账主要用提现功能"""
def pay_money(cash):
    user_choice1 = input('您购买的商品总价格为 %s 请确认是否结账[y]返回请按[b]' %cash)  # %count
    if user_choice1 == 'y':
        # 调用信用卡模块进行结账
        res = auth.creditcard_auth()
        creditcard_user = res[1]
        res1 = creditcard.withdrawals(creditcard_user)
        # 判断提现的钱数是否商品价格
        if res1 != None:
            if int(res1) < cash:
                print("您提取的余额不够支付账单、请再次提取")
                creditcard.withdrawals(creditcard_user)
            else:
                print("结账成功，购物车商品加入到数据库")
            pass
    elif user_choice1 == 'b':
        pass
    else:
        print("输入有误,请重新输入")
    return


exit_flag = False

while not exit_flag:
    index_page()

    index_user_choice = input('请输入您要进行的操作：')

    if index_user_choice == '0':
        login()
        exit_flag = True
    elif index_user_choice == '1':
        add_user()
        exit_flag = True
    elif index_user_choice == '2':
        print_product_list()
    else:
        print('输入操作无效！')

print('Begin The Shopping'.center(80, '-'), '\n')

#def shopping():
while True:
    if not user_list[user]['shop_car']:
        shop_car = []
        shop_car_list = []
    else:
        shop_car = user_list[user]['shop_car']
        shop_car_list = user_list[user]['shop_car_list']
    print_product_list()
    print("[查看购物车:c=check,退出商城:q=quit]", '\n')
    user_choice = input('请输入您想要购买的商品编号>>>: ')
    if user_choice.isdigit():
        user_choice = int(user_choice)
        if user_choice < len(product_list):
            p_item = product_list[user_choice]
            product = p_item[0]
            cash = p_item[1]
            if p_item not in shop_car:
                shop_car.append(p_item)
                shop_car_list.append(1)
                user_list[user]['shop_car'] = shop_car
                user_list[user]['shop_car_list'] = shop_car_list
                print('\033[32;1m 添加了：%s,价格是：%s\033[0m' % (product, cash), '\n')
                pay_money(cash)
            else:
                item_num = shop_car_list[shop_car.index(p_item)] + 1
                shop_car_list[shop_car.index(p_item)] = item_num
                user_list[user]['shop_car_list'] = shop_car_list
                print('\033[32;1m 在购物车上添加了：%s\033[0m' % (product, cash), '\n')
                pay_money(cash)
        else:
            print('你选择的商品不存在！', '\n')
    else:
        if user_choice == 'q' or user_choice == 'quit':
            printending()
            print('Bye %s' % user)
            wirte_logout()
            sys.exit()
        elif user_choice == 'c' or user_choice == 'check':
            printending()
        else:
            print('请输入合法字符！', '\n')