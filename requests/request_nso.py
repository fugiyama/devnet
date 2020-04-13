import requests

def main():
    #GET REQUESTS
    api_path = 'http://10.122.64.177:8181/api'
    basic_auth = ('admin','admin')

    accept_list = ['application/vnd.yang.api+json',
                    'application/vnd.yang.datastore+json',
                    'application/vnd.yang.data+json',
                    'application/vnd.yang.collection+json']

    get_headers = {'Accept':','.join(accept_list)}

    post_headers = {'Content-Type':'application/vnd.yang.data+json'}

    get_resp = requests.get(
        f"{api_path}/running/devices/device",
        auth=basic_auth,
        headers=get_headers
    )
    
    if get_resp.status_code != 200:
        raise requests.exceptions.HTTPError("Empty device list")

    devices = get_resp.json()['collection']['tailf-ncs:device']

    for dev in devices:
        loopbacks = dev['config']['tailf-ned-cisco-ios:interface']['loopback']

    lb_str =[]
    for lb_dict in loopbacks:
        lb_str.append(lb_dict['name'])
    
    print(f"Name: {dev['name']} IP: {dev['address']}",end ="  ")
    print(f"SSH port: {dev['port']} Loopback: {lb_str} ")

    new_loopback = {'tailf-ned-cisco-ios:Looback': [{'name':dev['port']}]}

    port_resp = requests.post(
        f"{api_path}/runnin/devices/device/{dev['name']}/config/interface",
        auth=basic_auth,
        headers=get_headers
        json=new_loopback,
    )

    if post_resp.ok:
        print(f"    - New loopback added to {dev['name']}")

if __name__ =='__main__':
    maint()