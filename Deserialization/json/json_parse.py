import json

jsonstr = '''
{
    "People": [
        {
            "id":"1",
            "FirstName":"Benjamin",
            "LastName":"Finkel",
            "Email":"ben.finkel@test.com"
        },
        {
            "id":"2",
            "FirstName":"Jane",
            "LastName":"Doe",
            "Email":"jane.doe@test.com"
        },
        {
            "id":"3",
            "FirstName":"Pat",
            "LastName":"Smith",
            "Email":"pat.smith@test.com"
        }



    ]

}
'''
#LOADING FROM A FILE
jsonobj_load = json.load(open('people.json'))
jsonobj = json.loads(jsonstr)

print(jsonobj)
