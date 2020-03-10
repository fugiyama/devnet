


from napalm import get_network_driver
import argparse
import sys

parser = argparse.ArgumentParser()
#CREATE THE ARGUMENT IP ADDRESS
parser.add_argument('-ip','--router_ip',help="Enter the ip address")
args = parser.parse_args()
#SELEC THE router_ip argument
device_ip = args.router_ip

# SELEC THE DRIVER
driver = get_network_driver('ios')
device = driver(username='cisco',
                password='cisco',
                optional_args={'port':22},
                hostname='10.122.64.251')

# CONNECT
device.open()
print("Running ........")
device.load_replace_candidate(filename='new_loopbacks.cfg') #<<<<<<<<<<<< ONLY DIFERENCE
diffs = device.compare_config()

if len(diffs) > 0:
    print(diffs)

    commit = input("Type COMMIT or ENTER to abort")
    if commit == "COMMIT":
        try:
            device.commit_config()

        except Exception as inst:
            print ('\n An error ocurred with the commit:')
            print(type(inst))
            sys.exit(inst)
            print()
        
        else:
            print("Config commited")
    
    else:
        sys.exit('Script aborted by user')
else:
    print("No changes needed")
    device.discard_config()

device.close()
