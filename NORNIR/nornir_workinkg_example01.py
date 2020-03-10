from nornir import InitNornir
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command , netmiko_send_config
from nornir.plugins.tasks.networking import napalm_get, napalm_configure
from nornir.core.filter import F

nr = InitNornir(config_file="config.yaml")

print_result(nr.run(task=netmiko_send_config, config_commands =['ip scp server enable']))
print_result(nr.run(task=napalm_configure, filename='defaultconf.cfg'))

'''
# OPEN CONFIG FILE
with open ('defaultconf.cfg','r') as file:
    commandlist = []
    for i in file.readlines():
        commandlist.append(i.strip('\n').strip())

# OPEN SEND CONFIGS
print_result(nr.run(task=netmiko_send_config, config_commands = commandlist))

# GETTERS
print_result(nr.run(task=napalm_get, getters=["facts"]))

# Get Output commands
result = nr.run(task=netmiko_send_command, command_string="show interfaces")

#Making filters
r1 = nr.filter(F(hostname__contains='192.168.99.10'))
'''