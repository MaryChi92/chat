from ipaddress import ip_address
from subprocess import Popen, PIPE

ipv4_1 = ip_address('23.13.253.71')
ipv4_2 = ip_address('91.198.174.192')
ipv4_3 = ip_address('5.200.46.11')
hosts_list = [ipv4_1, ipv4_2, ipv4_3]


def host_ping(hosts_list):
    for host in hosts_list:
        if not Popen(f'ping {host}', stdout=PIPE):
            print(f'Узел {host} недоступен')
        print(f'Узел {host} доступен')


host_ping(hosts_list)
