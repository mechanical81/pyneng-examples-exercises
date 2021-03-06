# -*- coding: utf-8 -*-
"""
Задание 7.1

Обработать строки из файла ospf.txt и вывести информацию по каждой строке в таком
виде на стандартный поток вывода:

Prefix                10.0.24.0/24
AD/Metric             110/41
Next-Hop              10.0.13.3
Last update           3d18h
Outbound Interface    FastEthernet0/0

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""


with open('ospf.txt') as f:
    for line in f:
        o, prefix, ad_metric, via, next_hop, last_update, intf = line.split()
        ad_metric = ad_metric.strip('[]')
        next_hop = next_hop.strip(',')
        last_update = last_update.strip(',')
        tmpl = f'''
        Prefix                {prefix}
        AD/Metric             {ad_metric}
        Next-Hop              {next_hop}
        Last update           {last_update}
        Outbound Interface    {intf}
        '''
        print(tmpl)

    