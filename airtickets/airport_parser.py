# coding:utf-8
from airtickets import settings

settings.configure()

import requests
from bs4 import BeautifulSoup



from mainapp.models import Airport



page = requests.get('https://en.wikipedia.org/wiki/List_of_busiest_airports_by_passenger_traffic')

soup = BeautifulSoup(page.content, 'html.parser')


tables = soup.findAll("table", {"class": "wikitable"})

def find_dict_in_list(list, key):
    r = ''
    try:
        r = next(item for item in list if item["name"] == key)
    except Exception as err:
        pass
    return r


parsed_data = []


table = tables[0]

for table in tables:
    body = table.find('tbody')
    rows = body.find_all('tr', recursive=False)

    for row in rows[1:]:
        columns = row.find_all('td')
        if not find_dict_in_list(parsed_data, columns[1].getText()):
            Airport.objects.create(name=columns[1].getText(), code=columns[4].getText().split('/')[0], location=columns[2].getText())
            parsed_data.append({'name':columns[1].getText(), 'code':columns[4].getText().split('/')[0], 'location':columns[2].getText()})

for row in parsed_data:
    print('name:', row['name'])
    print('code:', row['code'])
    print('location:', row['location'])
    print()

print(len(parsed_data))