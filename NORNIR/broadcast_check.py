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
    r = task.run(netmiko_send_command, command_string="show interfaces", use_genie=True)
    task.host["facts"] = r.result
    for slot in range(0,2):
        for port in range(0,4):
            print('## Ethernet' + str(slot) + "/" + str(port))
            broadcast_value = int(task.host['facts']['Ethernet' + str(slot) + "/" + str(port)]['counters']['in_broadcast_pkts'])
            print(broadcast_value)
            if broadcast_value == 0:
                print("Potential broadcast storm on " + task.host.hostname + "'s Ethernet" + str(slot) + "/" + str(port) + " interface")



def main() -> None:
    nr = InitNornir(config_file="config.yaml")
    result = nr.run(task=get_facts)
    #print_result(result)
    #import ipdb;
    #ipdb.set_trace()

if __name__ == '__main__':
    main()
