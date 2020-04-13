import csv
from nornir import InitNornir
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command , netmiko_send_config

header = ['hostname','ip','ios','uptime']
with open ('ios_ios.csv','w') as csv_file:
    output_writter = csv.writer(csv_file,delimiter=',',quotechar = '"', quoting=csv.QUOTE_MINIMAL)
    output_writter.writerow(header)
	
def get_facts(task):
    r = task.run(netmiko_send_command,command_string='show version', use_genie=True)
    task.host['facts'] = r.result
   #print(task.host)

    hostname = task.host['facts']['version']['hostname']
    image = task.host['facts']['version']['system_image']
    uptime = task.host['facts']['version']['uptime']

    print('+'*50 +'\n' + ' Hostname: {}\n Version: {}\n Uptime: {}\n'.format(hostname,image,uptime))
	
    with open ('ios_ios.csv','a') as csv_file:
        output_writter = csv.writer(csv_file,delimiter=',',quotechar = '"', quoting=csv.QUOTE_MINIMAL)
        output_writter.writerow([hostname,task.host,image,uptime])
	
def main():
    nr = InitNornir(config_file="config.yaml")
    result = nr.run(task=get_facts)
    print_result(result)
    end_result = nr.inventory.get_inventory_dict()

    failed_devices = []

    for ip in end_result['hosts'].keys():
        if end_result['hosts'][ip]['data'] == {}:
            failed_devices.append(str(ip) + '\n')

    with open ('failed_devices.csv','w') as file:
        file.writelines(failed_devices)
    
    #import ipdb
    #ipdb.set_trace()

if __name__ == "__main__":
    main()