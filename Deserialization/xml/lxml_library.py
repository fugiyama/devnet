from lxml import etree as ET


stream = open('people.xml','r')

xml = ET.parse(stream)

root = xml.getroot()

for e in root:
    print(ET.tostring(e))
    print('')
    print(e.get('id'))