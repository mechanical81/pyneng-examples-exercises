# -*- coding: utf-8 -*-
"""
Задание 15.3

Создать функцию convert_ios_nat_to_asa, которая конвертирует правила NAT
из синтаксиса cisco IOS в cisco ASA.

Функция ожидает такие аргументы:
- имя файла, в котором находится правила NAT Cisco IOS
- имя файла, в который надо записать полученные правила NAT для ASA

Функция ничего не возвращает.

Проверить функцию на файле cisco_nat_config.txt.

Пример правил NAT cisco IOS
ip nat inside source static tcp 10.1.2.84 22 interface GigabitEthernet0/1 20022
ip nat inside source static tcp 10.1.9.5 22 interface GigabitEthernet0/1 20023

И соответствующие правила NAT для ASA:
object network LOCAL_10.1.2.84
 host 10.1.2.84
 nat (inside,outside) static interface service tcp 22 20022
object network LOCAL_10.1.9.5
 host 10.1.9.5
 nat (inside,outside) static interface service tcp 22 20023

В файле с правилами для ASA:
- не должно быть пустых строк между правилами
- перед строками "object network" не должны быть пробелы
- перед остальными строками должен быть один пробел

Во всех правилах для ASA интерфейсы будут одинаковыми (inside,outside).
"""

import re
from pprint import pprint

def convert_ios_nat_to_asa(infile, outfile):
    cisco_regex = r'ip nat inside source static tcp (\S+) (\d+) interface \S+ (\d+)'
    asa_regex = (
        r'object network LOCAL_\1\n'
        r' host \1\n'
        r' nat (inside,outside) static interface service tcp \2 \3'
    )

    with open(infile) as f:
        asa_string = re.sub(cisco_regex, asa_regex, f.read())
    
    with open(outfile, 'w') as f:
        f.write(asa_string)



if __name__ == '__main__':
    convert_ios_nat_to_asa('cisco_nat_config.txt', 'asa_nat_config.txt')

