import requests
import csv
from bs4 import BeautifulSoup

input_file = csv.DictReader(open("postcode.csv"))
postcodes = [row['postcode'] for row in input_file]

dict_writer = csv.DictWriter(open('postcode.csv', 'a+', newline=''), ["postcode", "state", "long", "lat"])
if(len(postcodes) == 0): dict_writer.writeheader()

states = ['act', 'nsw', 'nt', 'qld', 'sa', 'tas', 'vic', 'wa']
# states = ['nsw']
for state in states:
    print(state)
    url = 'https://www.matthewproctor.com/full_australian_postcodes_' + state
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    table = soup.find('table')
    rows = table.find_all('tr')

    for row in rows:
        cells = row.find_all("td")
        if cells[1].string == 'Postcode':
            continue    
        if cells[4].text.strip() == '0' or cells[4].text.strip() == '':
            continue
        if cells[1].string not in postcodes:
            dict_writer.writerow({"postcode": cells[1].string, "state": cells[3].string, "long": cells[4].string, "lat": cells[5].string})
            postcodes.append(cells[1].string)
