# -*- coding: utf-8 -*-
"""
Задание 21.1a

Создать функцию parse_output_to_dict.

Параметры функции:
* template - имя файла, в котором находится шаблон TextFSM.
  Например, templates/sh_ip_int_br.template
* command_output - вывод соответствующей команды show (строка)

Функция должна возвращать список словарей:
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на выводе команды output/sh_ip_int_br.txt
и шаблоне templates/sh_ip_int_br.template.
"""

import textfsm
from pprint import pprint


def parse_output_to_dict(template, command_output):
    result = []
    with open(template) as tmpl_file:
        parser = textfsm.TextFSM(tmpl_file)
        header = parser.header
        parser_output = parser.ParseText(command_output)
        for item in parser_output:
            result.append( dict(zip(header, item)) )
    return(result)


if __name__ == '__main__':
    with open('output/sh_ip_int_br.txt') as show_output:
        pprint(parse_output_to_dict('templates/sh_ip_int_br.template', show_output.read()))