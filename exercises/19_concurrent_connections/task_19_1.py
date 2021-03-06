# -*- coding: utf-8 -*-
"""
Задание 19.1

Создать функцию ping_ip_addresses, которая проверяет пингуются ли IP-адреса.
Проверка IP-адресов должна выполняться параллельно в разных потоках.

Параметры функции ping_ip_addresses:
* ip_list - список IP-адресов
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для выполнения задания можно создавать любые дополнительные функции.

Для проверки доступности IP-адреса, используйте ping.

Подсказка о работе с concurrent.futures:
Если необходимо пинговать несколько IP-адресов в разных потоках,
надо создать функцию, которая будет пинговать один IP-адрес,
а затем запустить эту функцию в разных потоках для разных
IP-адресов с помощью concurrent.futures (это надо сделать в функции ping_ip_addresses).
"""


import subprocess
from concurrent.futures import ThreadPoolExecutor

def ping_ip_addresses(ip_list, limit = 3):
    ping_success = []
    ping_bad = []

    with ThreadPoolExecutor(max_workers = limit) as executor:
        future_list = []
        for ip_address in ip_list:
            future = executor.submit(is_ping_success, ip_address)
            future_list.append(future)
        for ip_address, future in zip(ip_list, future_list):
            if future.result():
                ping_success.append(ip_address)
            else:
                ping_bad.append(ip_address)
    
    return ping_success, ping_bad
        


def is_ping_success(ip_address):
    result = subprocess.run(['ping', '-c', '3', '-n', ip_address], stdout = subprocess.PIPE)
    if result.returncode == 0:
        return True
    else:
        return False


if __name__ == '__main__':
    ip_list = [
        '8.8.8.8',
        '128.0.0.1',
        '9.9.9.9',
        '128.0.0.2'
    ]

    print(ping_ip_addresses(ip_list, 3))