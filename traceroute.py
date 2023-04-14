import argparse
import json
import re
import subprocess
from urllib.request import urlopen

PRIVATE_IP = [
    ('10.0.0.0', '10.255.255.255'),
    ('100.64.0.0', '100.127.255.255'),
    ('127.0.0.0', '127.255.255.255'),
    ('172.16.0.0', '172.31.255.255'),
    ('192.168.0.0', '192.168.255.255')
]


class Information:
    def __init__(self, hop: int, ip: str):
        self.hop = hop
        self.ip = ip
        self.asn = ''
        self.country = ''
        self.provider = ''


def parse() -> str:
    """ Parsing command line arguments. """
    parser = argparse.ArgumentParser('Tracing of autonomous systems')
    parser.add_argument("address", help="IP-address or domain name")

    return parser.parse_args().address


def trace(address: str):
    """ Getting IP addresses with the traceroute utility and processing additional information. """
    data = subprocess.check_output(["traceroute", '-q', '1', '-w', '1', address]).decode('CP866')
    ip_pattern = r'(?<=\()[^\)]*'
    ip_addresses = re.findall(ip_pattern, data)

    print_title()

    for hop, line in enumerate(ip_addresses, 1):
        info = Information(hop, line)
        if is_public_ip_address(line):
            get_info(line, info)
        print_info(info)


def is_public_ip_address(address: str) -> bool:
    """ Check whether ip is in the range of private addresses. """
    for diapason in PRIVATE_IP:
        if diapason[0] <= address <= diapason[1]:
            return False
    return True


def get_info(ip: str, storage: Information):
    """Get information about provider, country and autonomous system. """
    info = json.load(urlopen(f"http://ipinfo.io/{ip}/json"))

    try:
        org = info['org'].split()
        storage.asn = org[0]
        storage.provider = ' '.join(org[1:])
    except KeyError:
        storage.asn = ''
        storage.provider = ''

    storage.country = info['country']


def print_info(info: Information):
    print(f'{info.hop}\t{info.ip}\t\t{info.asn}\t\t{info.country}\t{info.provider}')


def print_title():
    print(f'HOP\tIP\t\t\tAS\t\tCС\tPROVIDER\n{"-" * 120}')


if __name__ == '__main__':
    trace(parse())
