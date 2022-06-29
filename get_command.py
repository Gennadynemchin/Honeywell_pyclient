import socket
import sys


def get_command(command_ip, command_port):
    # open socket connection
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as command_socket:
            command_socket.connect((command_ip, command_port))
            recieve_command = command_socket.recv(256)
            print(recieve_command)
    except Exception:
        print('Command port connection has not been established. Abort operation')
        sys.exit()
    return recieve_command

get_command('192.168.11.61', 9301)
