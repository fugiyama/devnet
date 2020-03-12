from nornir import InitNornir
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command , netmiko_send_config
from nornir.core.filter import F


with open ('iplist','r') as file:
   iplist = file.read().splitlines()

output = []
for i in iplist:
    output.append(str(i)+''':
   hostname: '''+str(i)+'''
   groups:
     - routers
''')

with open ('hosts.yaml','w') as file:
    file.writelines(output)

nr = InitNornir(config_file="config.yaml")

interfaces = (nr.run(task=netmiko_send_command,command_string='sh run | i interface (.*)'))

for x in interfaces.keys():
    device = nr.filter(F(hostname__contains=x))
    print(x)
    if_cdp = ''
    interfaces_cdp = interfaces[x].result.replace('interface ','').splitlines()
    print(interfaces_cdp)
    print('Device : {} - Interfaces a configurar:\n     {}'.format(x,interfaces_cdp))

    for interface in interfaces_cdp:
        if 'Vlan' not in interface:
            if_cdp = (nr.run(task=netmiko_send_command,command_string = 'show cdp nei {} det | i Device|Platform'.format(interface)))
            print_result(if_cdp)

            for line in if_cdp[x].result.splitlines():
                    #cdp_hostname = if_cdp[x].result.splitlines()[if_cdp[x].result.splitlines().index(line) - 1]
                    #cdp_hostname = (cdp_hostname.replace(' ','').split(':')[1])
                if 'Device' in line:
                    cdp_hostname = line.split()[-1]
                    print(cdp_hostname)
                if 'Platform: Linux' in line:
                    print(line)
                    print('configuring interface {}'.format(interface))
                    print_result(device.run(task=netmiko_send_config, config_commands = ['interface '+ interface,'descr ' + cdp_hostname]))
