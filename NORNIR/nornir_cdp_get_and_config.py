from nornir import InitNornir
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command , netmiko_send_config


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


def get_facts(task):
    r = task.run(netmiko_send_command,command_string='show cdp neighbors detail', use_genie=True)
    task.host['facts'] = r.result
    print(task.host)
    
    for key in task.host['facts']['index'].keys():
        if 'Linux Unix' in task.host['facts']['index'][key]['platform']:
            print (task.host['facts']['index'][key]['device_id'])
            task.run(netmiko_send_config, config_commands = ['interface ' + task.host['facts']['index'][key]['local_interface'],
                                                                     'descrip ' + task.host['facts']['index'][key]['device_id'] + ' - ' +
                                                                     str(list(task.host['facts']['index'][key]['entry_addresses'].keys())[0])])
            
def main():
    nr = InitNornir(config_file="config.yaml")
    result = nr.run(task=get_facts)
    print_result(result)
    import ipdb
    ipdb.set_trace()

if __name__ == "__main__":
    main()
     