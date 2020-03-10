from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import napalm_get

nr = InitNornir(config_file="config.yaml")

result = nr.run(
    task=napalm_get, getters=["facts","interfaces"]
)

'''
result = nr.run(
    task=netmiko_send_command,command_string="show ip int br"
)
'''
print_result(result) 