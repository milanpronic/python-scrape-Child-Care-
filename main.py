import requests
import json
import csv

input_file = csv.DictReader(open("data.csv"))
ids = [row['id'] for row in input_file]

dict_writer = csv.DictWriter(open('data.csv', 'a+', newline=''), ["id", "name", "address", "email", "mobile", "phone", "website"])
if(len(ids) == 0): dict_writer.writeheader()

f = open('service1.txt')
for row in f:
    if(row[0:-1] in ids):
        continue
    print(row[0:-1])
    params = '{"serviceId":"%s","currentDayName":"tuesday","searchMode":"singular"}' % row[0:-1]
    url = 'https://search.childcarefinder.gov.au/services/?body=' + params
    headers = {'origin': 'https://www.childcarefinder.gov.au'}
    r = requests.get(url, headers = headers)
    response = json.loads(r.content)
    
    generic = response['hits']['hits'][0]['_source']['generic']
    info = {
        'id': row[0:-1],
        'name': generic['name'],
        'address': generic['address_info']['f_adr'],
        'email': generic['contact_info']['contact_email'],
        'mobile': generic['contact_info']['contact_mobile'],
        'phone': generic['contact_info']['contact_phone'],
        'website': generic['contact_info']['contact_url']
    }
    dict_writer.writerow(info)