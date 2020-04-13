
from nornir import InitNornir
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command , netmiko_send_config

header = ['hostname','ip','ios','uptime']
	
def get_facts(task):
    r = task.run(netmiko_send_command,command_string='show version', use_genie=True)
    task.host['facts'] = r.result
   #print(task.host)

    hostname = task.host['facts']['version']['hostname']
    image = task.host['facts']['version']['system_image']
    uptime = task.host['facts']['version']['uptime']

    print('+'*50 +'\n' + ' Hostname: {}\n Version: {}\n Uptime: {}\n'.format(hostname,image,uptime))
	
	with open ('ios_ios.csv','w') as csv_file:
    output_writter = csv.writer(csv_file,delimiter=',',quotechar = '"', quoting=csv.QUOTE_MINIMAL)
    output_writter.writerow([hostname,task.host,image,uptime])
	
def main():
    nr = InitNornir(config_file="config.yaml")
    result = nr.run(task=get_facts)
    print_result(result)
    import ipdb
    ipdb.set_trace()

if __name__ == "__main__":
    main()