# -*- coding: utf-8 -*-

"""
Задание 24.2b

Скопировать класс MyNetmiko из задания 24.2a.

Дополнить функционал метода send_config_set netmiko и добавить в него проверку
на ошибки с помощью метода _check_error_in_command.

Метод send_config_set должен отправлять команды по одной и проверять каждую на ошибки.
Если при выполнении команд не обнаружены ошибки, метод send_config_set возвращает
вывод команд.

In [2]: from task_24_2b import MyNetmiko

In [3]: r1 = MyNetmiko(**device_params)

In [4]: r1.send_config_set('lo')
---------------------------------------------------------------------------
ErrorInCommand                            Traceback (most recent call last)
<ipython-input-2-8e491f78b235> in <module>()
----> 1 r1.send_config_set('lo')

...
ErrorInCommand: При выполнении команды "lo" на устройстве 192.168.100.1 возникла ошибка "Incomplete command."

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
    command_output = r1.send_config_set('logging 0255.255.1')
    pprint(command_output)
