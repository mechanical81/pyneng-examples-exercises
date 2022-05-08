# -*- coding: utf-8 -*-
"""
Задание 21.4

Создать функцию send_and_parse_show_command.

Параметры функции:
* device_dict - словарь с параметрами подключения к одному устройству
* command - команда, которую надо выполнить
* templates_path - путь к каталогу с шаблонами TextFSM
* index - имя индекс файла, значение по умолчанию "index"

Функция должна подключаться к одному устройству, отправлять команду show
с помощью netmiko, а затем парсить вывод команды с помощью TextFSM.

Функция должна возвращать список словарей с результатами обработки
вывода команды (как в задании 21.1a):
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на примере вывода команды sh ip int br
и устройствах из devices.yaml.
"""

from pprint import pprint
from netmiko import ConnectHandler
from task_21_3 import parse_command_dynamic

def send_and_parse_show_command(device_dict, command, templates_path='templates', index='index'):
    attributes_dict = {
        'Command' : command,
        'Vendor' :  device_dict["device_type"]
    }
    with ConnectHandler(**device_dict) as ssh:
        ssh.enable()
        output = ssh.send_command(command)

        return parse_command_dynamic(output, attributes_dict, index, templates_path )



if __name__ == "__main__":
    r1_params = {
        "device_type": "cisco_ios",
        "host": "192.168.100.1",
        "username": "cisco",
        "password": "cisco",
        "secret": "cisco",
    }
    pprint(send_and_parse_show_command(r1_params, 'sh ip int br') )