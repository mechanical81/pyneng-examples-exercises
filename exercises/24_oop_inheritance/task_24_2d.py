# -*- coding: utf-8 -*-

"""
Задание 24.2d

Скопировать класс MyNetmiko из задания 24.2c или задания 24.2b.

Добавить параметр ignore_errors в метод send_config_set.
Если передано истинное значение, не надо выполнять проверку на ошибки и метод должен
работать точно так же как метод send_config_set в netmiko.
Если значение ложное, ошибки должны проверяться.

По умолчанию ошибки должны игнорироваться.


In [2]: from task_24_2d import MyNetmiko

In [3]: r1 = MyNetmiko(**device_params)

In [6]: r1.send_config_set('lo')
Out[6]: 'config term\nEnter configuration commands, one per line.  End with CNTL/Z.\nR1(config)#lo\n% Incomplete command.\n\nR1(config)#end\nR1#'

In [7]: r1.send_config_set('lo', ignore_errors=True)
Out[7]: 'config term\nEnter configuration commands, one per line.  End with CNTL/Z.\nR1(config)#lo\n% Incomplete command.\n\nR1(config)#end\nR1#'

In [8]: r1.send_config_set('lo', ignore_errors=False)
---------------------------------------------------------------------------
ErrorInCommand                            Traceback (most recent call last)
<ipython-input-8-704f2e8d1886> in <module>()
----> 1 r1.send_config_set('lo', ignore_errors=False)

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

    def send_config_set(self, commands, ignore_errors=True):
        if ignore_errors:
            return super().send_config_set(commands)
        else:
            full_command_output = ""
            if type(commands) == str:
                commands = [commands]
            for command in commands:
                command_output = super().send_config_set(command)
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
    command_output = r1.send_config_set('lo', ignore_errors=False)
    pprint(command_output)
