import csv
import requests
import json
import argparse
parser = argparse.ArgumentParser(description="A argument is required: start_idx")
parser.add_argument("-s", "--start_idx", type=int, help="'start index' counting from 1")
args = parser.parse_args()
if not args.start_idx:
    args.start_idx = 1

f = open("service.txt",'r+',encoding = 'utf-8')
services = [row[0:-1] for row in f]

input_file = csv.DictReader(open("postcode.csv"))
idx = 0
for row in input_file:
    idx+=1
    if(idx < args.start_idx):
        continue
    print(str(idx) + " postcode: " + row['postcode'])
    params = '{"filters":{"service_type":["ZCDC","ZFDC","ZOSH"]},"googleAddress":{"lat":%s,"lon":%s},"state":"%s","currentRadius":"7km","sortOrder":"order-tier","dayName":"tuesday","searchMode":"multiple"}' % (row['lat'], row['long'], row['state'])
    url = 'https://search.childcarefinder.gov.au/services/?body=' + params
    headers = {'origin': 'https://www.childcarefinder.gov.au'}
    r = requests.get(url, headers = headers)
    response = json.loads(r.content)
    
    print('\t' + str(len(response['hits']['hits'])))
    for service in response['hits']['hits']:
        if service['_id'] not in services:
            f.write(service['_id'] + "\n")
            services.append(service['_id'])
    