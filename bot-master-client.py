from enum import Enum
from hashlib import new
import socket
import os
import re
import platform
import socket
import struct

server_port = 12000

def recvall(sock, n)-> bytearray:
    # Helper function to recv n bytes or return None if EOF is hit
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data

def recv_msg(sock)->bytearray:
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    return recvall(sock, msglen)

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
                #bytes_readed = client_socket.recv(1024)
                #data = bytes_readed.decode()
                bytes_readed = recv_msg(client_socket)
                print("Bytes received: "+str(len(bytes_readed)))
                data = bytes_readed.decode()
                for line in data.splitlines():
                    print(line)
                if data == "Closing connection":
                    break
            except Exception as e:
                print("Exception! "+str(e))

                break


if __name__ == '__main__':
    main()
