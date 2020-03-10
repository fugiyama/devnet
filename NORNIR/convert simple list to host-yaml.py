
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