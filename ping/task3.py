from ipaddress import ip_address
from subprocess import Popen, PIPE

from tabulate import tabulate

ipv4_1 = ip_address(input('IP-address: '))
number = int(input('Range: '))

type_hosts_dict = {"reachable": [],
                   "unreachable": []
                   }


def host_range_ping(host, number):
    try:
        last_octet = int(str(host).split('.')[-1])
    except Exception as e:
        print(e)
    else:
        if last_octet + number <= 255:
            for i in range(number):
                if not Popen(f'ping {host}', stdout=PIPE):
                    type_hosts_dict["unreachable"].append(host)
                type_hosts_dict["reachable"].append(host)
                host += 1
        else:
            print('Sorry, the range is too broad')


host_range_ping(ipv4_1, number)

print(tabulate(type_hosts_dict, headers='keys', tablefmt='pipe'))
