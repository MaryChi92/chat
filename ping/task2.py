from ipaddress import ip_address
from subprocess import Popen, PIPE

ipv4_1 = ip_address('23.13.253.71')


def host_range_ping(host, number):
    try:
        last_octet = int(str(host).split('.')[-1])
    except Exception as e:
        print(e)
    else:
        if last_octet + number <= 255:
            for i in range(number):
                if not Popen(f'ping {host}', stdout=PIPE):
                    print('Узел недоступен')
                print('Узел доступен')
                host += 1
        else:
            print('Sorry, the range is too broad')


host_range_ping(ipv4_1, 5)
host_range_ping(ipv4_1, 300)
