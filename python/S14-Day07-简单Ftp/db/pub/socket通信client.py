#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Colin Yao
#客户端
import socket
client = socket.socket() #定义协议类型,相当于生命socket类型,同时生成socket连接对象
client.connect(('localhost',62000))
while True:
    data = client.recv(1024)#这里是字节1k
    print("recv:>",data.decode())
    msg = input(">>>").strip()
    if len(msg) ==0:continue
    client.send(msg.encode("utf-8"))
client.close()
