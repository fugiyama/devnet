from netmiko import ConnectHandler
import argparse
from datetime import datetime

devices = {}
'''
devices = {IP : { WANIF : { ZONE:[ ACL01, ALC02 ] }}}

'''
output = []
WARNINGS = []
ssh_error = []
not_zone = []


#ACL TO DEFINE WHAT TO CHECK
ports_entry = [21,22,23,80]
permited_ports = []
protocols_tcp = ['bgp', 'chargen', 'cmd', 'daytime', 'discard', 'domain', 'echo', 'exec', 'finger', 'ftp', 'ftp-data', 
                'gopher', 'hostname', 'ident', 'irc', 'klogin', 'kshell', 'login', 'lpd', 'msrpc', 'ntp', 'onep-plain',
                'onep-tls', 'pim-auto-rp', 'pop2', 'pop3', 'smtp', 'sunrpc', 'syslog', 'tacacs', 'talk',
                'telnet', 'time', 'uucp', 'whois', 'www']


with open ('output.csv','w') as f:
    f.write('ip,tunnel,interface,zbf,acl\n')

with open ('WARNINGS.csv','w') as f:
    f.write('ip,acl,tcp-port\n')

with open ('iplist','r') as f:
    iplist = (f.read().splitlines())


ssh_connection = {
'device_type': 'cisco_ios',
'host':'' ,
'username': 'cisco',
'auth_timeout': 15,
'timeout': 15,
'password': 'cisco',
'port':'22'
}

start_time = datetime.now()

for ip in iplist:
    ACL_double_check = []
    try:
        print('[*] Connecting : {}'.format(ip))
        ssh_connection['host'] = ip
        connection = ConnectHandler(**ssh_connection)
        device_ip = connection.host
        interfaces = connection.send_command('show ip int br | i Tunnel').split()
        #print(interfaces)
    except Exception as e:
        print('<!> [AUTH ERROR] - Trying next device...')
        ssh_error.append(ip)
        continue

    #wan_interfaces = []
    #tunnel_interfaces = []

    for tunnel in interfaces:
        try:
            if "Tunnel" in tunnel:

                wanif = connection.send_command('show run int ' + tunnel + ' | i tunnel source').split()[-1]
                '''
                GET THE ZONE, ZONE-PAIR AND CLASS BY IFACE WAN
                '''
                try:
                    zone = connection.send_command('show run int ' + wanif + ' | i zone-member').split()[-1]
                    #print(zone)
                    zone_pair = connection.send_command('sh zone-pair security source ' + zone + ' destination self | i Zone-pair name').split()[-1]
                    #print(zone_pair)
                    zone_class_map = connection.send_command('sh policy-map  type inspect zone-pair ' + zone_pair +' | section Class-map:').splitlines()
                    #print(zone_class_map)
            
                except Exception as e:
                    '''
                    WRITE NULL IF THE IFACE WAN DOESNT HAVE A ZONE
                    '''
                    with open ('output.csv','a+') as f:
                        
                        f.writelines(device_ip + ',' + tunnel + ',' + wanif + ',NULL\n')
                        devices = {}
                        output = []
                        not_zone.append(ip)
                        continue
                    #output.append(device_ip + ',' + tunnel + ',' + wanif + ',NULL\n')
                
                
                devices[device_ip] = {wanif:{}}
                devices[device_ip][wanif] = {zone :[]}

                for line in zone_class_map:
                    '''
                    GET ALL THE ACLs CONFIGURED ON THE SERVICE POLICY ATTACHED TO THE ZONE-PAIR
                    '''
                    if "Match: access-group name" in line:
                        #print(line)
                        ACL = str(line.split()[-1])
                        ACL_double_check.append(ACL)
                        devices[device_ip][wanif][zone].append(ACL)
                  
                with open ('output.csv','a') as f:
                    '''
                    WRITE IN THE CSV FORMAT USING THE OUTPUT LIST
                    '''
                    zone_acls = devices[device_ip][wanif][zone]
                    zone_acls_str = ','.join([str(acl) for acl in zone_acls])
                    f.writelines(device_ip + ',' + tunnel + ',' + wanif + ',' + zone + ',' + zone_acls_str +'\n')
                #output.append(device_ip + ',' + tunnel + ',' + wanif + ',' + zone + ',' + zone_acls_str +'\n')

        except Exception as e:
            print('<!> Interfaces {} doesnt have source-wan'.format(tunnel))
            continue

    ###############################################################################################
    ############################# CHECK ACL SESSION ############################################### 
    ###############################################################################################

    ACL_double_check = list(dict.fromkeys(ACL_double_check))
    #print(ACL_double_check)

    #CHECK THE PORTS OF ACL
    try:    
        for acl_entry in ACL_double_check:
            ACL_OUTPUT = connection.send_command('sh ip access ' + acl_entry ).splitlines()
            # RESET THE PERMISSIONS OF THE ACL
            permited_ports = []
            
            for line in ACL_OUTPUT:
                if 'permit' and  'tcp' and  'eq' in line:
                    protocol = (line.split()[-1])
                    permited_ports.append(protocol)
                    

                elif 'permit ip any any' in line:
                    print("WARNING ACL {} IS ALLOWING ALL PORTS".format( acl_entry )) 
                    with open ('WARNINGS.csv','a') as f:
                        f.writelines(device_ip + ','  + acl_entry + ','+ 'permit ip any any\n')
                        
            for x in ports_entry:
                if (str(x) in permited_ports) or  (str(x) in protocols_tcp:
                    #print("WARNING ACL {}  PORT {} IS ALLOWED".format(acl_entry,x))
                    with open ('WARNINGS.csv','a') as f:
                        f.writelines(device_ip + ',' + acl_entry + ',' + str(x) + '\n')

    except Exception as e:
        continue
 



                    
                
    devices = {}
    output = []

    connection.disconnect()



end_time = datetime.now()
total_time = end_time - start_time

logs =  ['''
++++++++++++++++++++++++++++++++++++++++++++++++++

[*] - Device fail to connect: [ {} ] 
{}
[*] - Devices without zone: [ {} ] 
{}

 

Total Time: {}

++++++++++++++++++++++++++++++++++++++++++++++++++
'''.format(len(ssh_error),ssh_error, len(not_zone), not_zone, total_time)]


with open ('logs.txt', 'w') as f:
    f.writelines(logs)








exit()


