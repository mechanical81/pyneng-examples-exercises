# -*- coding: utf-8 -*-
"""
Задание 9.3a

Сделать копию функции get_int_vlan_map из задания 9.3.

Дополнить функцию: добавить поддержку конфигурации, когда настройка access-порта
выглядит так:
    interface FastEthernet0/20
        switchport mode access
        duplex auto

То есть, порт находится в VLAN 1

В таком случае, в словарь портов должна добавляться информация, что порт в VLAN 1
Пример словаря:
    {'FastEthernet0/12': 10,
     'FastEthernet0/14': 11,
     'FastEthernet0/20': 1 }

У функции должен быть один параметр config_filename, который ожидает
как аргумент имя конфигурационного файла.

Проверить работу функции на примере файла config_sw2.txt

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""

def get_int_vlan_map(config_filename):
    access = {}
    trunk = {}
    
    with open(config_filename) as f:
        for line in f:
            line = line.strip()
            if line.startswith('interface') and not 'Vlan' in line:
                _, intf = line.split()
                access[intf] = 1
            if line.startswith('switchport access vlan'):
                _, _, _, vlan = line.split()
                access[intf] = int(vlan)
            if line.startswith('switchport trunk allowed vlan'):
                _, _, _, _, vlan_str = line.split()
                vlans = [int(vl) for vl in vlan_str.split(',')]
                trunk[intf] = vlans
                del access[intf]
    return access, trunk


print(get_int_vlan_map('config_sw2.txt'))