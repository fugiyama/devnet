Filter Based on the host name

from nornir.core.filter import F

In [9]: nr.inventory.hosts
Out[9]: {'R1LAB': Host: R1LAB, 'R2LAB': Host: R2LAB}

R2 = nr.filter(name='R2LAB')

Filter Based on groups

In [15]: routers = nr.filter(F(groups__contains='routers'))

In [16]: routers.inventory.hosts
Out[16]: {'R1LAB': Host: R1LAB, 'R2LAB': Host: R2LAB}

Filter Based on tags

isr4300 = nr.filter(F(tags__contains='isr4300'))

Filter Based on tags and other atributes

isr4300 = nr.filter(F(tags__contains='isr4300') & F(groups__contains='NEW_YORK'))

Example:
result =  isr4300.run(task=netmiko_send_command,command_string='show arp')
print_result (result)

