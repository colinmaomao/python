#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Time:2017/12/6 15:52
__Author__ = 'Sean Yao'
import pika
import time
import subprocess
import platform

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost'))

# rabbitmq 设有权限的连接
# connection = pika.BlockingConnection(pika.ConnectionParameters(
# host='192.168.1.105',credentials=pika.PlainCredentials('admin', 'admin')))

channel = connection.channel()
channel.queue_declare(queue='127.0.0.1')
os_res = platform.system()

# def command(cmd, task_id):
def command(cmd):
    if os_res == 'Windows':
        res = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        msg = res.stdout.read().decode('gbk')
        if len(msg) == 0:
            msg = res.stderr.read().decode('gbk')
        print(msg)
        return msg

    else:
        res = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(res)
        msg = res.stdout.read().decode()
        if len(msg) == 0:
            msg = res.stderr.read().decode()
        return msg

def on_request(ch, method, props, body):
    cmd = body.decode()
    respone = command(cmd)
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id=props.correlation_id),
                     body=respone)
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='127.0.0.1')
print(" [x] Awaiting RPC requests")
channel.start_consuming()
