# -*- coding: utf-8 -*-
"""
Задание 7.2a

Сделать копию скрипта задания 7.2.

Дополнить скрипт: Скрипт не должен выводить на стандартрый поток вывода команды,
в которых содержатся слова из списка ignore.

При этом скрипт также не должен выводить строки, которые начинаются на !.

Проверить работу скрипта на конфигурационном файле config_sw1.txt.
Имя файла передается как аргумент скрипту.

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

from sys import argv 

ignore = ["duplex", "alias", "configuration"]

file = argv[1]

ignore_set = set(ignore)

with open(file) as f:
    for line in f:
        line_set = set(line.split())
        xset = line_set & ignore_set
        if not line.startswith('!') and not xset:
            print(line.rstrip())
