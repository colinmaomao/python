#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Time:2017/12/6 15:52
__Author__ = 'Sean Yao'
import pika
import uuid

class CommandToRabbitmq(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, command, host):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        ack = self.channel.basic_publish(exchange='',
                                         routing_key=host,
                                         properties=pika.BasicProperties(
                                             reply_to=self.callback_queue,
                                             correlation_id=self.corr_id),
                                         body=str(command))
        while self.response is None:
            self.connection.process_data_events()

        task_id = self.corr_id
        res = self.response.decode()
        tmp_dict[task_id] = res
        print('task_id: %s host: %s cmd: %s ' % (self.corr_id, host, command))
        return self.corr_id, self.response.decode()

def help():
    print('Usage: run "df -h" --hosts 127.0.0.1 192.168.84.66 ')
    print('       check_task 54385061-aa3a-400f-8a21-2be368e66493 ')
    print('       check_task_all')


def start(command_input):
    command_list = command_input.split()
    if command_list[0] == 'check_task':
        try:
            print(tmp_dict[command_list[1]])
            del tmp_dict[command_list[1]]
        except IndexError:
            help()
    elif command_list[0] == 'run':
        # 获取命令主机,并循环执行
        try:
            ip_hosts_obj = command_input.split('run')
            hosts_obj = (ip_hosts_obj[1].split('--hosts'))
            hosts = hosts_obj[1].strip().split()
            command = command_input.split("\"")[1]
            for host in hosts:
                try:
                    command_rpc.call(command, host)
                except TypeError and AssertionError:
                    break
        except IndexError:
            print('-bash: %s command not found' % command_input)
            help()
    elif command_list[0] == 'check_task_all':
        for index, key in enumerate(tmp_dict.keys()):
            print(index, 'task_id: %s' % key)
    elif command_list[0] == 'help':
        help()
    else:
        print('-bash: %s command not found' % command_input)
        help()


command_rpc = CommandToRabbitmq()
exit_flag = True
tmp_dict = {}
help()
while exit_flag:
    command_input = input('请输入命令>>>:').strip()
    if len(command_input) == 0:
        continue
    else:
        start(command_input)