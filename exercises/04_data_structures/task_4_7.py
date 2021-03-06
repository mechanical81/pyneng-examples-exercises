# -*- coding: utf-8 -*-
"""
Задание 4.7

Преобразовать MAC-адрес в строке mac в двоичную строку такого вида:
'101010101010101010111011101110111100110011001100'

Полученную новую строку вывести на стандартный поток вывода (stdout) с помощью print.

Ограничение: Все задания надо выполнять используя только пройденные темы.

Предупреждение: в разделе 4 тесты можно легко "обмануть" сделав нужный вывод,
без получения результатов из исходных данных с помощью Python.
Это не значит, что задание сделано правильно, просто на данном этапе сложно иначе
проверять результат.
"""

mac = "AAAA:BBBB:CCCC"

template = "{:b}"*12

mac_str = mac.replace(":","")
mac_list = list(mac_str)
print(template.format(
    int(mac_list[0],16),
    int(mac_list[1],16),
    int(mac_list[2],16),
    int(mac_list[3],16),
    int(mac_list[4],16),
    int(mac_list[5],16),
    int(mac_list[6],16),
    int(mac_list[7],16),
    int(mac_list[8],16),
    int(mac_list[9],16),
    int(mac_list[10],16),
    int(mac_list[11],16)
    ))