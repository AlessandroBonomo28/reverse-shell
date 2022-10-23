from ast import arg
from typing import Dict, Tuple
import re
class Parser():
    """Il parser si occupa di dividere il comando in due parti: il comando principale e un dizionario di tutti i suoi argomenti
    
    Methods
    -------
    parse(command: str) -> Tuple[str, Dict[str, any]]
        Il metodo parse ritorna il comando principale e un dizionario di tutti i suoi argomenti
    """

    def parse(self, command: str) -> Tuple[str, Dict[str, any]]:
        """Il metodo parse ritorna il comando principale e un dizionario di tutti i suoi argomenti"""
        betw_apici = re.search('\'(.*)\'',command)
        to_replace = ""
        if betw_apici:
            to_replace = betw_apici.group(1)
            #print("subcmd = "+subcmd)
            command = command.replace("'"+to_replace+"'","xREPLACEx")
        
        splitted_command = command.split(" ")
        command_length = len(splitted_command)
        arguments_dict = {}
        
        if len(splitted_command) <= 0 or command == "":
            raise RuntimeError("Nessun comando inserito")

        main_command = splitted_command[0]
        
        if len(splitted_command) >= 2:
            for i in range(1, command_length):
                current_elem = splitted_command[i]
                
                if current_elem.startswith("-"):
                    if i+1 > command_length - 1 or splitted_command[i+1].startswith("-"):
                        arguments_dict[current_elem] = True
                    else:
                        arguments_dict[current_elem] = splitted_command[i+1]
                
                if current_elem.startswith("/"):
                    if i+1 > command_length - 1 or splitted_command[i+1].startswith("/"):
                        arguments_dict[current_elem] = True
                    else:
                        arguments_dict[current_elem] = splitted_command[i+1]
                
        for i in arguments_dict.keys():
            if arguments_dict[i] == "xREPLACEx":
                arguments_dict[i] = to_replace
        return [main_command, arguments_dict]


"""p = Parser()
print(p.parse("shellexec -c 'ls -l'"))
print(p.parse("shellexec -c 'dir /d'"))
print(p.parse("ls -l 10"))"""
