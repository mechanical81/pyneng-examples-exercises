# -*- coding: utf-8 -*-
"""
Задание 12.1

Создать функцию ping_ip_addresses, которая проверяет пингуются ли IP-адреса.

Функция ожидает как аргумент список IP-адресов.

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для проверки доступности IP-адреса, используйте команду ping (запуск ping через subprocess).
IP-адрес считается доступным, если выполнение команды ping отработало с кодом 0 (returncode).
Нюансы: на Windows returncode может быть равен 0 не только, когда ping был успешен,
но для задания нужно проверять именно код. Это сделано для упрощения тестов.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""

import subprocess

def ping_ip_addresses(ip_list):
    ip_list_ok = []
    ip_list_notok = []
    for ip in ip_list:
        reply = subprocess.run(['ping', '-c', '3', '-n', ip])
        if reply.returncode == 0:
            ip_list_ok.append(ip)
        else:
            ip_list_notok.append(ip)
    return ip_list_ok, ip_list_notok

if __name__ == '__main__':
    ip_list = ['8.8.8.8', '127.0.0.1', '10.10.10.10', '10.10.10.11']
    print(ping_ip_addresses(ip_list))
