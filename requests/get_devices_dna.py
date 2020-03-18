import requests





def get_token():
    api_path = 'https://sandboxdnac.cisco.com/dna'
    auth = ('devnetuser','Cisco123!')
    headers = {"Content-Type":"application/json"}

    auth_resp = requests.post (
        f"{api_path}/system/api/v1/auth/token", auth=auth, headers=headers
    )

    auth_resp.raise_for_status()
    token = auth_resp.json()['Token']
    return token


def get_devices(token):
    api_path = 'https://sandboxdnac.cisco.com/dna'
    auth = ('devnetuser','Cisco123!')
    headers = {"Content-Type":"application/json",
                "X-Auth-Token":token}

    devices_get = requests.get(
        f"{api_path}/intent/api/v1/network-device", auth=auth, headers=headers
    )

    devices = devices_get.json()['response']

    return devices



def main():

    token = get_token()
    devices = get_devices(token)
    #print(token)
    #print(devices)
    #import ipdb
    #ipdb.set_trace()
    print(f'We have { len(devices) } devices.\n'+('#'*50))
    for x in devices:
        print(f'''\rNAME: { x['hostname'] }
        \rMODEL: { x['platformId'] }
        \rSN: { x['serialNumber'] }
        \rIP: { x['managementIpAddress'] }
        ''')



if __name__ == '__main__':
    main()