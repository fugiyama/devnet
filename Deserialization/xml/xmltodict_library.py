import xmltodict

stream = open('people.xml','r')

xml = xmltodict.parse(stream.read())

for e in xml['People']['Person']:
    print(e)
