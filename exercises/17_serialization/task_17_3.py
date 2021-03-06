# -*- coding: utf-8 -*-
"""
Задание 17.3

Создать функцию parse_sh_cdp_neighbors, которая обрабатывает
вывод команды show cdp neighbors.

Функция ожидает, как аргумент, вывод команды одной строкой (не имя файла).
Функция должна возвращать словарь, который описывает соединения между устройствами.

Например, если как аргумент был передан такой вывод:
R4>show cdp neighbors

Device ID    Local Intrfce   Holdtme     Capability       Platform    Port ID
R5           Fa 0/1          122           R S I           2811       Fa 0/1
R6           Fa 0/2          143           R S I           2811       Fa 0/0

Функция должна вернуть такой словарь:
{'R4': {'Fa 0/1': {'R5': 'Fa 0/1'},
        'Fa 0/2': {'R6': 'Fa 0/0'}}}

Интерфейсы должны быть записаны с пробелом. То есть, так Fa 0/0, а не так Fa0/0.


Проверить работу функции на содержимом файла sh_cdp_n_sw1.txt
"""

import re
from pprint import pprint

def parse_sh_cdp_neighbors(show_output):
    re_hostname = r'(\S+)>show cdp neighbors'
    match = re.search(re_hostname, show_output)
    if match:
        l_hostname = match.group(1)
    else:
        return None
    
    re_cdp = r'(?P<r_hostname>\S+)\s+(?P<l_intf>\S+ \S+)\s+\d+.+ (?P<r_intf>\S+ \S+)\n'
    matches = re.finditer(re_cdp, show_output)
    result = {}
    if matches:
        sub_result = {}
        for m in matches:
            sub_result[m.group('l_intf')] = { m.group('r_hostname') : m.group('r_intf') }
        result[l_hostname] = sub_result
    return result


if __name__ == '__main__':
    with open('sh_cdp_n_r2.txt') as f:
        pprint( parse_sh_cdp_neighbors(f.read()) )