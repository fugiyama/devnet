
#!/usr/bin/python3
from netmiko import ConnectHandler
import time

def device_config():
    #Command list to send
    cmd_list = ['ip route 1.1.1.1 255.255.255.255 null0',
                'ip route 1.1.1.2 255.255.255.255 null0',
                'ip route 1.1.1.3 255.255.255.255 null0'
    ]

    ssh_connection = { 
    'device_type': 'cisco_ios',
    'host':'10.122.64.201',
    'username': 'cisco',
    'password': 'cisco',
    'port':'2211'
     } 

    connection = ConnectHandler(**ssh_connection)

    #Check if connection is config mode
    if connection.check_config_mode() == False:
        connection.config_mode()

    output = connection.send_config_set(cmd_list)
    connection.exit_config_mode()
    return output



if __name__ == "__main__":
    print(device_config())