# -*- coding: utf-8 -*-

"""
Задание 23.1a

Скопировать и изменить класс IPAddress из задания 23.1.

Добавить два строковых представления для экземпляров класса IPAddress.
Как дожны выглядеть строковые представления, надо определить из вывода ниже:

Создание экземпляра
In [5]: ip1 = IPAddress('10.1.1.1/24')

In [6]: str(ip1)
Out[6]: 'IP address 10.1.1.1/24'

In [7]: print(ip1)
IP address 10.1.1.1/24

In [8]: ip1
Out[8]: IPAddress('10.1.1.1/24')

In [9]: ip_list = []

In [10]: ip_list.append(ip1)

In [11]: ip_list
Out[11]: [IPAddress('10.1.1.1/24')]

In [12]: print(ip_list)
[IPAddress('10.1.1.1/24')]

"""


class IPAddress:
    def __init__(self, ip_mask):
        
        ip_exception = "Incorrect IPv4 address"
        mask_exception = "Incorrect mask"

        self.ip, self.mask = ip_mask.split('/')
        
        octets = self.ip.split('.')
        if len(octets) != 4:
            raise ValueError(ip_exception)

        try:
            for octet in self.ip.split('.'):
                if not 0 <= int(octet) <= 255:
                    raise ValueError(ip_exception)
        except ValueError:
            raise ValueError(ip_exception)

        try:
            if not 8 <= int(self.mask) <= 32:
                raise ValueError(mask_exception)
        except ValueError:
            raise ValueError(mask_exception)
        self.mask = int(self.mask)

    def __str__(self):
        return(f"IP address {self.ip}/{self.mask}")

    def __repr__(self):
        return(f"IPAddress('{self.ip}/{self.mask}')")


if __name__ == '__main__':
    ip1 = IPAddress('10.1.1.1/24')
    print(ip1)

    ip_list = []
    ip_list.append(ip1)
    print(ip_list)