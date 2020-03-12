import yaml
from yaml import load, load_all

stream = open('people.yaml','r')
documents = load_all(stream, Loader=yaml.FullLoader)

print(type(documents))

try:
    for doc in documents:
        for x in doc['people']:
            print('NAME: ' + x['FirstName'] +'\nEMAIL : '+ x['Email'])
except (TypeError) as e:
    print ("KEY IS NOT EQUAL PEOPLE")
