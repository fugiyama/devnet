import csv
from pprint import pprint
from nornir import InitNornir
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command , netmiko_send_config
from tqdm import tqdm

header = ['hostname','ip','model','serial','ios','uptime','reload_reason']
with open ('ios_ios.csv','w') as csv_file:
    output_writter = csv.writer(csv_file,delimiter=',',quotechar = '"', quoting=csv.QUOTE_MINIMAL)
    output_writter.writerow(header)
	
def get_facts(task,netmiko_getversion):
    r = task.run(netmiko_send_command,command_string='show version', use_textfsm=True)
    task.host['facts'] = r.result
    netmiko_getversion.update()
    #print(task.host)

    hostname = task.host['facts'][0]['hostname']
    image = task.host['facts'][0]['running_image']
    uptime = task.host['facts'][0]['uptime']
    serial = task.host['facts'][0]['serial']
    model = task.host['facts'][0]['hardware']
    reload_reason = task.host['facts'][0]['reload_reason']

    #print('+'*50 +'\n' + ' Hostname: {}\n Version: {}\n Uptime: {}\n'.format(hostname,image,uptime))
	
    with open ('ios_ios.csv','a') as csv_file:
        output_writter = csv.writer(csv_file,delimiter=',',quotechar = '"', quoting=csv.QUOTE_MINIMAL)
        output_writter.writerow([hostname,task.host,model,serial,image,uptime,reload_reason])
	
def main():
    nr = InitNornir(config_file="config.yaml")
    with tqdm(total=len(nr.inventory.hosts), desc="gathering version",) as netmiko_getversion:

        result = nr.run(task=get_facts,
                        netmiko_getversion=netmiko_getversion)
                        
        #print_result(result)


        end_result = nr.inventory.get_inventory_dict()

        failed_devices = []

        for ip in end_result['hosts'].keys():
            if end_result['hosts'][ip]['data'] == {}:
                failed_devices.append(str(ip) + '\n')

        with open ('failed_devices.csv','w') as file:
            file.writelines(failed_devices)
        
        
        
        #import ipdb
        #ipdb.set_trace()

    print('+'*50 + 
        '''\n[*] Failed devices: ''')
    for ip in failed_devices:
        print(ip.strip(),end=',')

if __name__ == "__main__":
    main()