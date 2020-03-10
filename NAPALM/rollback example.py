

from napalm import get_network_driver
import sys
import argparse

parser =argparse.ArgumentParser()
parser.add_argument('-ip','--router_ip',help="Enter the IP address")
args = parser.parse_args()
device_ip = args.router_ip


driver = get_network_driver('ios')

device = driver(username='cisco',
                password='cisco',
                optional_args={'port':22},
                hostname=device_ip)

device.open()
print('Running ......')
device.load_merge_candidate(filename='new_loopbacks.cfg')
diffs = device.compare_config()

if len(diffs) > 0:
    print(diffs)

    commit = input("Type COMMIT or ENTER to exit: ")
    if commit == 'COMMIT':
        try:
            device.commit_config()

        except Exception as inst:
            print("\n An error ocurred with the commit: ")
            print(type(inst))
            sys.exit(inst)
            print()

        else:
            print('Config Commited')
    else:
        sys.exit('Scrpt aborted by user: ')
else:
    print('No changes needed')
    device.discard_config()
    sys.exit()
    device.close()

rollback = input("Type ROLLBACK to rever or ENTER to abort: ")

if rollback == "ROLLBACK":
    try:
        device.rollback()

    except Exception as inst:
        print('\n An error ocurred with the rollback')
        print(type(inst))
        sys.exit(inst)
    else:
        print('Configuration Reverted')
else:
    sys.exit()

device.close()

