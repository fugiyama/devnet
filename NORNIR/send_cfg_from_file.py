#By IPvZERO
#https://github.com/IPvZero/IPvZero/blob/master/Nornir_Templates_Video/runbook2.py

from nornir import InitNornir
from nornir.plugins.functions.text import print_result, print_title
from nornir.plugins.tasks.networking import netmiko_send_command, netmiko_send_config

nr = InitNornir('config.yaml', dry_run=True)

def basic(test):
    test.run(task=netmiko_send_config, config_file = 'swt_default_cfg')
    test.run(task=netmiko_send_command, command_string ='show archive log conf all')

results = nr.run(task=basic)

print_title('CONFIGURING BASIC CFG')
print_result(results)
