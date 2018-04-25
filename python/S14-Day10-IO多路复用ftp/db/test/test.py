#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Colin Yao
import socket, os, sys, platform, json, time, errno, random, progressbar
BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from conf import setting

server_address = ('localhost', 10000)
#server_address = ('192.168.84.130', 10000)
socks = [socket.socket(socket.AF_INET, socket.SOCK_STREAM) for i in range(500)]

def High_Concurrency():
    try:
        print('connecting to %s port %s' % server_address)
        print('login time : %s' % (time.strftime("%Y-%m-%d %X", time.localtime())))
        while True:
            try:
                global action, file_name, file_path
                sending_msg_list = []
                sending_msg = input('[root@select_ftp_client]# ')
                sending_msg_list = sending_msg.split()
                action = sending_msg_list[0]
                if len(sending_msg_list) == 0:
                    continue
                elif len(sending_msg_list) == 1:
                    if sending_msg_list[0] == "exit":
                        print('logout')
                        break
                    else:
                        print(time.strftime("%Y-%m-%d %X", time.localtime()),
                              '-bash : %s command not found' % sending_msg_list[0])
                else:
                    if platform.system() == 'Windows':
                        try:
                            file_path = sending_msg_list[1]
                            file_list = sending_msg_list[1].strip().split('\\')
                            file_name = file_list[-1]
                        except IndexError:
                            pass
                    elif platform.system() == 'Linux':
                        try:
                            file_path = sending_msg_list[1]
                            file_list = sending_msg_list[1].strip().split('/')
                            file_name = file_list[-1]
                        except IndexError:
                            pass
                    if action == "put":
                        put()

                    elif action == "get":
                        get()
                    else:
                        print(time.strftime("%Y-%m-%d %X", time.localtime()), '[+]client:-bash: %s:'
                              % sending_msg_list[0], 'command not found')

            except ConnectionResetError and ConnectionRefusedError and OSError and IndexError as e:
                print(time.strftime("%Y-%m-%d %X", time.localtime()), '[+]client: -bash :', e, 'Restart client')
                High_Concurrency()

    except ConnectionResetError and ConnectionRefusedError  as e:
        print(time.strftime("%Y-%m-%d %X", time.localtime()), '[+]client: -bash :', e)

def put():
    start_time = time.time()
    for client in socks:
        client.connect(server_address)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            file_size = os.path.getsize(file_path)
            data_header = {"client": {
                "action": "put",
                "file_name": file_name,
                "size": file_size}}
            client.send(json.dumps(data_header).encode())
            print(time.strftime("%Y-%m-%d %X", time.localtime()), '[+]server: -bash : %s '
                  % client.recv(1024).decode())
            with open(file_path, 'rb') as file_object:
                try:
                    for line in file_object:
                        client.sendall(line)
                    file_object.close()
                except IOError as e:
                    if e.errno != errno.EAGAIN:
                        raise
                    else:
                        time.sleep(0.1)
            print(client.recv(1024).decode())
        else:
            print(time.strftime("%Y-%m-%d %X", time.localtime()),
                  '[+]client: -bash :%s : No such file' % file_name)
        client.close()
        end_time = time.time()
        print('上传并发运算时间>>>:', start_time - end_time)


def get():
    start_time = time.time()
    for client in socks:
        client.connect(server_address)
        os.chdir(setting.client_download_path)
        data_header = {"client": {
            "action": "get",
            "file_name": file_name,
            "size": 0}}
        client.send(json.dumps(data_header).encode())
        data = client.recv(1024)
        if data.decode() == '404':
            print(time.strftime("%Y-%m-%d %X", time.localtime()),
                  '[+]server: -bash : %s : No such file' % (file_path))
        else:
            print(time.strftime("%Y-%m-%d %X", time.localtime()),
                  "[+]server: -bash : File ready to get File size is :", data.decode())
            new = random.randint(1, 100000)
            file_object = open((file_name + '.' + (str(new))), 'wb')
            received_size = 0
            file_size = int(data.decode())
            while received_size < file_size:
                if file_size - received_size > 1024:
                    size = 1024
                elif file_size < 1024:
                    size = file_size
                else:
                    size = file_size - received_size
                recv_data = client.recv(size)
                received_size += len(recv_data)
                file_object.write(recv_data)
            else:
                file_object.flush()
                file_object.close()
                #time.sleep(0.1)
                print(time.strftime("%Y-%m-%d %X", time.localtime()),
                      "[+]client: -bash :File get done File size is :", file_size)
    end_time = time.time()
    print('下载并发运算时间>>>:', start_time - end_time)