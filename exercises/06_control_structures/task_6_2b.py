# -*- coding: utf-8 -*-
"""
Задание 6.2b

Сделать копию скрипта задания 6.2a.

Дополнить скрипт: Если адрес был введен неправильно, запросить адрес снова.

Если адрес задан неправильно, выводить сообщение: 'Неправильный IP-адрес'
Сообщение "Неправильный IP-адрес" должно выводиться только один раз,
даже если несколько пунктов выше не выполнены.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""
while True:
    ip = input('Введите IP адрес: ')
    ip_good = True
    
    iplist = ip.split('.')
    if len(iplist) != 4:
            ip_good = False

    for octet in iplist:
        if octet.isnumeric() and 0 <= int(octet) <= 255:
            continue
        else:
            ip_good = False
    
    if ip_good:
        o1 = int(ip.split('.')[0])
        if 1 <= o1 <= 223:
            print('unicast')
        elif 224 <= o1 <= 239:
            print('multicast')
        elif ip == '255.255.255.255':
            print('local broadcast')
        elif ip == '0.0.0.0':
            print('unassigned')
        else:
            print('unused')
        break

    else:
        print('Неправильный IP-адрес')
