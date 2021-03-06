# -*- coding: utf-8 -*-
"""
Задание 7.2b

Переделать скрипт из задания 7.2a: вместо вывода на стандартный поток вывода,
скрипт должен записать полученные строки в файл

Имена файлов нужно передавать как аргументы скрипту:
 * имя исходного файла конфигурации
 * имя итогового файла конфигурации

При этом, должны быть отфильтрованы строки, которые содержатся в списке ignore
и строки, которые начинаются на '!'.

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

from sys import argv 

ignore = ["duplex", "alias", "configuration"]
infile, outfile = argv[1:3]

ignore_set = set(ignore)

with open(infile) as f, open(outfile, 'w') as f_out:
    for line in f:
        line_set = set(line.split())
        xset = line_set & ignore_set
        if not line.startswith('!') and not xset:
            f_out.write(line)
