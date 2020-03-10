from napalm.base import get_network_driver
driver = get_network_driver('iosxr')
dev = driver(hostname='r1', username='admin',
             password='admin')
dev.open()
dev.load_merge_candidate(filename='ACL_SAMPLE.cfg')
dev.commit_config()
dev.close()


no ipv4 access-list ACCESS_OUT
ipv4 access-list ACCESS_OUT
 10 permit tcp any any eq domain
 20 remark udp any any eq dns
 30 permit tcp any any eq www
 40 remark tcp any any eq https