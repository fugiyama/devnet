from netmiko import ConnectHandler

ssh_connection = { 
'device_type': 'cisco_ios',
'host':'10.122.64.201',
'username': 'cisco',
'password': 'cisco',
'port':'2211'
    } 

net_connect = ConnectHandler(**ssh_connection)

command = 'ping'

output = net_connect.send_command_timing(command)
if "Protocol [ip]:" in output:
    output = net_connect.send_command_timing("\n")
    if "Target IP address:" in output:
        output = net_connect.send_command_timing("192.168.99.1\n")
        if "Repeat count [5]:" in output:
            output = net_connect.send_command_timing("1\n")
            if "Datagram size [100]:" in output:
                output = net_connect.send_command_timing("1500\n")
                if "Timeout in seconds [2]:" in output:
                    output = net_connect.send_command_timing("\n")
                    if "Extended commands [n]:" in output:
                        output = net_connect.send_command_timing("y\n")
                        if "Source address or interface:" in output:
                            output = net_connect.send_command_timing("\n")
                            if "Type of service [0]:" in output:
                                output = net_connect.send_command_timing("\n")
                                if "Set DF bit in IP header? [no]:" in output:
                                    output = net_connect.send_command_timing("y\n")
                                    if "Validate reply data? [no]:" in output:
                                        output = net_connect.send_command_timing("\n")
                                        if "Data pattern [0xABCD]:" in output:
                                            output = net_connect.send_command_timing("\n")                            
                                            if "Loose, Strict, Record, Timestamp, Verbose[none]:" in output:
                                                output = net_connect.send_command_timing("V\n")
                                                if "Loose, Strict, Record, Timestamp, Verbose[V]:" in output:
                                                    output = net_connect.send_command_timing("\n")
                                                    if "Sweep range of sizes [n]:" in output:
                                                        output = net_connect.send_command_timing("y\n")
                                                        if "Sweep min size [36]:" in output:
                                                            output = net_connect.send_command_timing("1400\n")
                                                            if "Sweep max size [18024]:" in output:
                                                                output = net_connect.send_command_timing("1500\n")
                                                                if "Sweep interval [1]:" in output:
                                                                    output = net_connect.send_command_timing("\n")

outputlist = output.splitlines()
for i in outputlist:
    if 'Success rate is' in  i:
        print(i)
        
net_connect.disconnect()