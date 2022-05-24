# -*- coding: utf-8 -*-

"""
Задание 24.2c

Скопировать класс MyNetmiko из задания 24.2b.
Проверить, что метод send_command кроме команду, принимает еще и дополнительные
аргументы, например, strip_command.

Если возникает ошибка, переделать метод таким образом, чтобы он принимал
любые аргументы, которые поддерживает netmiko.


In [2]: from task_24_2c import MyNetmiko

In [3]: r1 = MyNetmiko(**device_params)

In [4]: r1.send_command('sh ip int br', strip_command=False)
Out[4]: 'sh ip int br\nInterface                  IP-Address      OK? Method Status                Protocol\nEthernet0/0                192.168.100.1   YES NVRAM  up                    up      \nEthernet0/1                192.168.200.1   YES NVRAM  up                    up      \nEthernet0/2                190.16.200.1    YES NVRAM  up                    up      \nEthernet0/3                192.168.230.1   YES NVRAM  up                    up      \nEthernet0/3.100            10.100.0.1      YES NVRAM  up                    up      \nEthernet0/3.200            10.200.0.1      YES NVRAM  up                    up      \nEthernet0/3.300            10.30.0.1       YES NVRAM  up                    up      '

In [5]: r1.send_command('sh ip int br', strip_command=True)
Out[5]: 'Interface                  IP-Address      OK? Method Status                Protocol\nEthernet0/0                192.168.100.1   YES NVRAM  up                    up      \nEthernet0/1                192.168.200.1   YES NVRAM  up                    up      \nEthernet0/2                190.16.200.1    YES NVRAM  up                    up      \nEthernet0/3                192.168.230.1   YES NVRAM  up                    up      \nEthernet0/3.100            10.100.0.1      YES NVRAM  up                    up      \nEthernet0/3.200            10.200.0.1      YES NVRAM  up                    up      \nEthernet0/3.300            10.30.0.1       YES NVRAM  up                    up      '

"""

import re

from netmiko.cisco.cisco_ios import CiscoIosSSH
from pprint import pprint


class ErrorInCommand(Exception):
    """
    Исключение генерируется, если при выполнении команды на оборудовании,
    возникла ошибка.
    """


class MyNetmiko(CiscoIosSSH):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.enable()

    def _check_error_in_command(self, command, command_output):
        regexp = r"% (.+)\n*"
        match = re.search(regexp, command_output)
        if match:
            error_msg = match[1]
            except_msg = (
                f'При выполнении команды "{command}" '
                f'на устройстве {self.host} '
                f'возникла ошибка "{error_msg}"'
            )
            raise ErrorInCommand(except_msg)

    def send_command(self, command,  *args, **kwargs):
        command_output = super().send_command(command, *args, **kwargs)
        self._check_error_in_command(command, command_output)
        return command_output

    def send_config_set(self, commands, *args, **kwargs):
        full_command_output = ""
        if type(commands) == str:
            commands = [commands]
        for command in commands:
            command_output = super().send_config_set(command, *args, **kwargs)
            self._check_error_in_command(command, command_output)
            full_command_output += command_output
        self.exit_config_mode()
        return full_command_output


device_params = {
    "device_type": "cisco_ios",
    "ip": "192.168.100.1",
    "username": "cisco",
    "password": "cisco",
    "secret": "cisco",
}


if __name__ == "__main__":
    r1 = MyNetmiko(**device_params)
    command_output = r1.send_command('sh ip int br', strip_command=False)
    pprint(command_output)
