from napalm import get_network_driver
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-ip","--router_ip",help="Enter device ip address")
args = parser.parse_args()
device_ip = args.router_ip

driver = get_network_driver('ios')
device = driver(username='cisco',
                password='cisco',
                optional_args= {'port':22},
                hostname=device_ip)

device.open()
get_facts = device.get_facts()

device.close()
print (get_facts)