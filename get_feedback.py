# test_client.py
import telnetlib
import time
import socket



def get_verify(host, port):
    tn = telnetlib.Telnet(host, port)
    result = tn.read_until(b'</VerificationReport>')
    return result


def get_command_port(host, port):
    tn = telnetlib.Telnet(host, port)
    result = tn.read_until(b'</')
    return result



if __name__ == '__main__':
    while True:
        #print(get_command_port('192.168.78.180', 9301))
        print(get_verify('192.168.78.180', 9302))

