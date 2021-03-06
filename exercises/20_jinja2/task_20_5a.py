# -*- coding: utf-8 -*-
"""
Задание 20.5a

Создать функцию configure_vpn, которая использует
шаблоны из задания 20.5 для настройки VPN на маршрутизаторах
на основе данных в словаре data.

Параметры функции:
* src_device_params - словарь с параметрами подключения к устройству 1
* dst_device_params - словарь с параметрами подключения к устройству 2
* src_template - имя файла с шаблоном, который создает конфигурацию для строны 1
* dst_template - имя файла с шаблоном, который создает конфигурацию для строны 2
* vpn_data_dict - словарь со значениями, которые надо подставить в шаблоны

Функция должна настроить VPN на основе шаблонов
и данных на каждом устройстве с помощью netmiko.
Функция возвращает кортеж с выводом команд с двух
маршрутизаторов (вывод, которые возвращает метод netmiko send_config_set).
Первый элемент кортежа - вывод с первого устройства (строка),
второй элемент кортежа - вывод со второго устройства.

При этом, в словаре data не указан номер интерфейса Tunnel,
который надо использовать.
Номер надо определить самостоятельно на основе информации с оборудования.
Если на маршрутизаторе нет интерфейсов Tunnel,
взять номер 0, если есть взять ближайший свободный номер,
но одинаковый для двух маршрутизаторов.

Например, если на маршрутизаторе src такие интерфейсы: Tunnel1, Tunnel4.
А на маршрутизаторе dest такие: Tunnel2, Tunnel3, Tunnel8.
Первый свободный номер одинаковый для двух маршрутизаторов будет 5.
И надо будет настроить интерфейс Tunnel 5.

Для этого задания тест проверяет работу функции на первых двух устройствах
из файла devices.yaml. И проверяет, что в выводе есть команды настройки
интерфейсов, но при этом не проверяет настроенные номера тунелей и другие команды.
Они должны быть, но тест упрощен, чтобы было больше свободы выполнения.
"""


import yaml
import re
from netmiko import ConnectHandler
from pprint import pprint
from task_20_5 import create_vpn_config

data = {
    "tun_num": None,
    "wan_ip_1": "192.168.100.1",
    "wan_ip_2": "192.168.100.2",
    "tun_ip_1": "10.0.1.1 255.255.255.252",
    "tun_ip_2": "10.0.1.2 255.255.255.252",
}


def send_show_command(device, command):
    with ConnectHandler(**device) as ssh:
        ssh.enable()
        output = ssh.send_command(command)
        return output

def send_config_command(device, command):
    with ConnectHandler(**device) as ssh:
        ssh.enable()
        output = ssh.send_config_set(command)
        return output

def min_free_num(list1, list2):
    max_list1 = max(list1) if list1 else 0
    max_list2 = max(list2) if list2 else 0
    if max_list1 > max_list2:
        max_num = max_list1
    else:
        max_num = max_list2
    for num in range(max_num + 1):
        if (num not in list1) and (num not in list2):
            break
    return num



def configure_vpn(src_device_params, dst_device_params, src_template, dst_template, vpn_data_dict):
    show_tunnels_command = 'show run | include Tunnel'
    show_out_1 = send_show_command(src_device_params, show_tunnels_command)
    show_out_2 = send_show_command(dst_device_params, show_tunnels_command)
    regexp = r'interface Tunnel(\d+)'
    tunnel_nums_1 = re.findall(regexp, show_out_1)
    tunnel_nums_2 = re.findall(regexp, show_out_2)
    tunnel_nums_1_int = [int(item) for item in tunnel_nums_1]
    tunnel_nums_2_int = [int(item) for item in tunnel_nums_2]
    data_dict = vpn_data_dict.copy()
    data_dict['tun_num'] = min_free_num(tunnel_nums_1_int, tunnel_nums_2_int)

    tmpl_src, tmpl_dst = create_vpn_config(src_template, dst_template, data_dict)
    output1 = send_config_command(src_device_params, tmpl_src.split('\n'))
    output2 = send_config_command(dst_device_params, tmpl_dst.split('\n'))
    
    return output1, output2


if __name__ == '__main__':
    with open('20_jinja2/devices.yaml') as f:
        devices = yaml.safe_load(f)
    
    # print(min_free_num( [0, 1, 2, 6], [] ))

    output = configure_vpn(
        devices[0],
        devices[1],
        '20_jinja2/templates/gre_ipsec_vpn_1.txt',
        '20_jinja2/templates/gre_ipsec_vpn_2.txt',
        data
    )

    pprint(output)

