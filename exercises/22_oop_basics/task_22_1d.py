# -*- coding: utf-8 -*-

"""
Задание 22.1d

Изменить класс Topology из задания 22.1c

Добавить метод add_link, который добавляет указанное соединение, если его еще
 нет в топологии.
Если соединение существует, вывести сообщение "Такое соединение существует",
Если одна из сторон есть в топологии, вывести сообщение
"Cоединение с одним из портов существует"


Создание топологии
In [7]: t = Topology(topology_example)

In [8]: t.topology
Out[8]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [9]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))

In [10]: t.topology
Out[10]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R1', 'Eth0/4'): ('R7', 'Eth0/0'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [11]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))
Такое соединение существует

In [12]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/5'))
Cоединение с одним из портов существует


"""


from pprint import pprint


topology_example = {
    ("R1", "Eth0/0"): ("SW1", "Eth0/1"),
    ("R2", "Eth0/0"): ("SW1", "Eth0/2"),
    ("R2", "Eth0/1"): ("SW2", "Eth0/11"),
    ("R3", "Eth0/0"): ("SW1", "Eth0/3"),
    ("R3", "Eth0/1"): ("R4", "Eth0/0"),
    ("R3", "Eth0/2"): ("R5", "Eth0/0"),
    ("SW1", "Eth0/1"): ("R1", "Eth0/0"),
    ("SW1", "Eth0/2"): ("R2", "Eth0/0"),
    ("SW1", "Eth0/3"): ("R3", "Eth0/0"),
}


class Topology:
    def __init__(self, topology_dict):
        self.topology = self._normalize(topology_dict)
    
    def _normalize(self, topology_dict):
        result = {}
        for key, val in topology_dict.items():
            if key not in result.values():
                result[key] = val
        return result
    
    def delete_link(self, intf1, intf2):
        if self.topology.get(intf1) == intf2:
            del self.topology[intf1]
        elif self.topology.get(intf2) == intf1:
            del self.topology[intf2]
        else:
            print("Такого соединения нет")
    
    def delete_node(self, hostname):
        is_deleted = False
        links = list(self.topology.items())
        for key, val in links:
            if key[0] == hostname or val[0] == hostname:
                del self.topology[key]
                is_deleted = True
        if not is_deleted:
            print("Такого устройства нет")
    
    def add_link(self, intf1, intf2):
        get_intf1 = self.topology.get(intf1)
        get_intf2 = self.topology.get(intf2)
        if get_intf1 == intf2 or get_intf2 == intf1:
            print("Такое соединение существует")
        elif get_intf1 or get_intf2:
            print("Cоединение с одним из портов существует")
        else:
            self.topology[intf1] = intf2

            

if __name__ == '__main__':
    top = Topology(topology_example)
    pprint(top.topology)
    top.add_link(('R3', 'Eth0/2'), ('R5', 'Eth0/0'))
    print('=' * 25)
    pprint(top.topology)