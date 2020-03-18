from nornir import InitNornir
from nornir.plugins.functions.text import print_result
import requests


def fetch_and_parse_cdp_neighbors(task):
    url = f"https://{{task.host.hostname}}/restconf/data/Cisco-IOS-XE-cdp-oper:cdp-neighbor-details"
    
    headers = {"Accept": "application/yang-data+json"}
    
    response = requests.get(url, headers=headers,auth=(task.host.username, task.host.password), verify = False)

    data = response.json()["Cisco-IOS-XE-cdp-oper:cdp-neighbor-details"]

    return response(host=task.host, result=data)


def main():
    nr = InitNornir('config.yaml')
    print(nr.inventory.hosts)
    result = nr.run(fetch_and_parse_cdp_neighbors)
    print_result(result)


if __name__ == '__main__':
    main()