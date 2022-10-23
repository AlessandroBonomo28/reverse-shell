from cmath import sin
from datetime import datetime

from typing import List






class CommandExecutioner():
    """Il command executioner permette di eseguire una una collezione di funzioni configurate dall'utente"""
    def __init__(self, cmd_to_function: dict):
        self.cmd_to_function = cmd_to_function
    def execute(self, command: str, args:dict = {})-> list:
        if self.exists(command):
            return self.cmd_to_function[command](args)
        else: raise Exception("Command '"+command+"' does not exits")
    def exists(self, command : str) -> bool:
        if command in self.cmd_to_function: 
            return True
        else: 
            return False
    def get_command_list(self)-> list:
        return list(self.cmd_to_function.keys())

"""
x = ServerFunctions()
x.fun_names['saluto']()
exe = CommandExecutioner(x.fun_names)
print(exe.cmd_to_function)
exe.execute("saluto")
"""