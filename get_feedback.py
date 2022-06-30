import telnetlib


def get_verify(host, port):
    results = []
    reports = open('reports.xml', 'w')
    tn = telnetlib.Telnet(host, port)
    result = tn.interact()
    if result:
        results.append(result)
        reports.write(str(result))
    reports.close()
    return result


if __name__ == '__main__':
    while True:
        get_verify('192.168.78.180', 9302)
