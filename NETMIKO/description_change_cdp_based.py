

#!/usr/bin/python3
from datetime import datetime
import argparse
from netmiko import ConnectHandler


'''
parser =argparse.ArgumentParser()
parser.add_argument('-ip','--router_ip',help="Enter the IP address")
args = parser.parse_args()
device_ip = args.router_ip
'''

start_time = datetime.now()
first_ip = '192.168.99.101'
cdpbiglist = {first_ip:[]}
device_validator = [first_ip]
to_connect_devices = []
connected_devices = []
device_error = []

def SSH_CONNECTION(IP):
    global connection
    
    for x in to_connect_devices:
        if x == IP:
            to_connect_devices.remove(IP)        

    connected_devices.append(IP)
    ssh_connection = { 
        'device_type': 'cisco_ios',
        'host':IP,
        'username': 'cisco',
        'password': 'cisco',
        'port':'22'
    } 
    connection = ConnectHandler(**ssh_connection)


def GET_CDP_INFO():
    position_cont = 0
    if connection.host not in cdpbiglist.keys():
        cdpbiglist[connection.host] = []

    cdp_entry = connection.send_command('show cdp nei det').splitlines()
    
    for line in cdp_entry:
        if 'Device ID:' in line:
            device_name = line.split()[2]
            device_ip = cdp_entry[cdp_entry.index(line) + 2].strip().split()[2]
            cdpbiglist[connection.host].append([device_ip,device_name])
            info_appended = True
        elif ('Interface: ' in line) and (info_appended == True):
            device_interface = line.strip().split()[1].strip(',')
            cdpbiglist[connection.host][position_cont].append(device_interface)
            info_appended = False
            position_cont += 1

    for x in cdpbiglist[connection.host]:
        to_connect_devices.append(x[0])

    
#Fix interfaces descriptions
def FIX_DESCRIPTION(neighbor_ip=first_ip):
    for x in cdpbiglist[neighbor_ip]:
        connection.config_mode()
        print('[*] - Configuring Description for Neighbor: {} - {}'.format(x[1], x[0]))
        connection.send_command_timing('interface {}'.format(x[2]))
        connection.send_command_timing('description Connection to - {} - {}'.format(x[1], x[0]))
    connection.exit_config_mode()
    connection.disconnect()

SSH_CONNECTION(first_ip)
GET_CDP_INFO()
FIX_DESCRIPTION()

while len(to_connect_devices) > 0: 
    for neighbor_ip in to_connect_devices:
        if neighbor_ip in connected_devices:
            try:
                for item in to_connect_devices:
                    to_connect_devices.remove(neighbor_ip)
                break
            except Exception as E:
                continue
        else:
            try:
                print('[*] Connecting to Neighbor : {}'.format(neighbor_ip))
                SSH_CONNECTION(neighbor_ip)
            except Exception as E:
                print('<!> ERROR {}. Trying next...'.format(neighbor_ip))
                device_error.append(neighbor_ip)
                continue
            
            GET_CDP_INFO()
            FIX_DESCRIPTION(neighbor_ip)
            print('<OK> {}'.format(connected_devices))
            print('<!> {} Remaining ...'.format(len(to_connect_devices)))

end_time = datetime.now()
total_time = end_time - start_time
print('\n-------------------------------------------------')
print('Configured Devices: {} \n {}'.format(len(connected_devices),connected_devices))
print('\n-------------------------------------------------')
print('ERROR Devices: \n{}'.format(device_error))
print('\n-------------------------------------------------')
print('Total Time: {}'.format(total_time))






exit()

'''


{'First_ip':[['IP', 'NAME'], 
            ['IP', 'NAME'], 
            ['IP', 'NAME']],
 'Second_IP':[['IP', 'NAME'],
            ['IP', 'NAME'],
            ['IP', 'NAME']],
 'Tird_NAME':[['IP', 'NAME'],
            ['IP', 'NAME'],
            ['IP', 'NAME']]}

