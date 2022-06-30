import threading
import argparse
import socket
import sys
import telnetlib
from time import sleep


parser = argparse.ArgumentParser()

parser.add_argument("-a", "--address", type=str, help="Printer IP address")
parser.add_argument("-p", "--port", type=int, help="Printer port")
parser.add_argument("-c", "--count", type=int, help="How many codes you are going to print")
parser.add_argument("-t", "--template", type=str, help="Pathname of template")
parser.add_argument("-f", "--filename", type=str, help="Pathname of SN's")
args = parser.parse_args()


def get_verify(host, port):
    tn = telnetlib.Telnet(host, port)
    result = tn.read_until(b'</VerificationReport\n')
    reports = open('reports.xml', 'w')
    reports.write(str(result))
    return result


def send_to_zpl(host_zpl=args.address, port_zpl=args.port, until_counter=args.count, zpl_in=args.template, filename=args.filename):
    print(host_zpl, port_zpl, until_counter, zpl_in, filename)
    #open template file as one string
    try:
        with open(zpl_in, 'r') as zpl:
            template = zpl.read().replace('\n', '')
    except FileNotFoundError:
        print(f'File {zpl} does not exist. Check pathname and try again')


    #open file with SGTINs
    try:
        codes_to_print = open(filename, "r")
    except FileNotFoundError:
        print(f'File {filename} does not exist. Check pathname and try again')
    #open socket connection
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host_zpl, port_zpl))

            #iterating over the file with codes
            for count, line in enumerate(codes_to_print):
                gtin = line[4:18] #get gtin from file
                code = line[23:29] #get code field 21 from file
                crypto = line[34:38] #get crypto field 93 from file

                char_to_replace = {"{gtin}": str(gtin), "{code}": str(code), "{crypto}": str(crypto)}

                template_gtin = template.replace("{gtin}", str(gtin))
                template_code = template_gtin.replace("{code}", str(code))
                template_crypto = template_code.replace("{crypto}", str(crypto))

                s.sendall(template_crypto.encode())
                print(f'{template_crypto} sent, code number {count + 1}')
                sleep(0.4)


                if count == until_counter - 1:
                    break
            s.close()
    except Exception:
        print('Connection has not been established. Abort operation')
        sys.exit()
    codes_to_print.close()



def main():

    if None in [args.address, args.port, args.count, args.template, args.filename]:
        address = str(input('Enter IP address: '))
        port = int(input('Enter port: '))
        count = int(input('How many codes you are going to print: '))
        template = str(input('Template pathname: '))
        filename = str(input('Codes pathname: '))
        sleep(1)
        send_to_zpl(address, port, count, template, filename)
    else:
        send_to_zpl()
procs=[]

if __name__ == '__main__':
    #output = threading.Thread(target=get_verify, args=('192.168.78.180', 9302)).start()
    input = threading.Thread(target=send_to_zpl, args=('192.168.78.180', 9100, 25, 'zpl.txt', 'sn.csv')).start()