
from napalm import get_network_driver

driver =  get_network_driver('ios')

device = driver(username='cisco',
                password='cisco',
                optional_args = {'port':22},
                hostname='10.0.1.1')

device.open()

def check_bgp_states():
    command_bgp_state_mpls =  ['sho log | i  neighbor 192.168.100.1 Down']
    command_bgp_state_inet =  ['sho log | i  neighbor 192.168.200.1 Down']

    bgp_state_mpls = device.cli(command_bgp_state_mpls)
    bgp_state_mpls = bgp_state_mpls['sho log | i  neighbor 192.168.100.1 Down'].splitlines()
    
    bgp_state_inet = device.cli(command_bgp_state_inet)
    bgp_state_inet = bgp_state_inet['sho log | i  neighbor 192.168.200.1 Down'].splitlines()
    
    print ('BGP INET CAIU {} \nBGP MPLS CAIU {} '.format(len(bgp_state_inet), len(bgp_state_mpls )))
    if len(bgp_state_inet) > 2:
        print("ABRIR CHAMADO COM OPERADORA INTERNET LOCAL. HOUVERAM {} FALHAS NO BGP".format(len(bgp_state_inet)))
    if len(bgp_state_mpls) > 2: 
        print("ABRIR CHAMADO COM OPERADORA MPLS. HOUVERAM {} FALHAS NO BGP".format(len(bgp_state_mpls)))


check_bgp_states()
device.close()