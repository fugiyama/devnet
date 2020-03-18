from nornir import InitNornir
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command , netmiko_send_config
from nornir.core.filter import F
import csv

def dev_info(task):
    r = task.run(netmiko_send_command, command_string='show ver', use_genie=True)
    task.host['facts'] = r.result
    serial  = task.host['facts']['version']['chassis_sn']
    hoster = task.host['facts']['version']['hostname']

    with open ('test.csv','a') as csvfile:
        writer = csv.writer(csvfile)
        csvdata = ('TEST',task.host.hostname, serial, hoster)
        writer.writerow(csvdata)

def main() -> None:
    nr= InitNornir('config.yaml')
    result = nr.run(task=dev_info)
    print_result(result)
    #import ipdb;
    #ipdb.set_trace()

if __name__ == '__main__':
    main()

