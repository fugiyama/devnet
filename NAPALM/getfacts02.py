from napalm import get_network_driver 
import argparse

parser =argparse.ArgumentParser()
parser.add_argument("-ip","--router_ip",help="Enter the ip address")
args = parser.parse_args()
device_ip = args.router_ip

driver = get_network_driver('ios')
device = driver(username='cisco',
                password='cisco',
                optional_args={'port':22},
                hostname=device_ip)

device.open()
print('Running .....')
router_dic = device.get_facts()

for i in router_dic:
    if type(router_dic[i]) == list:
        print(i)
        for k in router_dic[i]:
            print('\t - {}'.format(k))
            
    else:
        print('{} : {}'.format(i, router_dic[i]))


device.close()

