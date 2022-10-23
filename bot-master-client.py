from enum import Enum
from hashlib import new
import socket
import os
import re
import platform
import socket


server_port = 12000

def main():
    ip_address = "127.0.0.1"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:

        client_socket.connect((ip_address, server_port))

        data = client_socket.recv(1024)
        identity_response = data.decode()
        print(identity_response)
        
        while True:
            try:
                cmd = input("Waiting for command ('help' to list commands):")
                if cmd == "":
                    print("Cannot send empty command.")
                    continue
                client_socket.send(cmd.encode())

                print("Sent command '"+cmd+"' to server ...")
                
                data = client_socket.recv(1024).decode()
                print(data)
                if data == "Closing connection":
                    break
            except Exception as e:
                print("Exception! "+str(e))

                break


if __name__ == '__main__':
    main()
