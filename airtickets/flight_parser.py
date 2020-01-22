# coding:utf-8
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "airtickets.settings")
django.setup()

from airtickets import settings
import requests
from bs4 import BeautifulSoup
from mainapp.models import Flight, Aircompany, Airport

page = requests.get('https://www.aeroflot.ru/ru-ru/flight/ways_map_table')

soup = BeautifulSoup(page.content, 'html.parser')


tables = soup.findAll("table", {'class':'tariff_list'})

def find_dict_in_list(list, key):
    r = ''
    try:
        r = next(item for item in list if item["to"] == key)
    except Exception as err:
        pass
    return r


parsed_data = []


for table in tables:
    rows = table.find_all('tr')
    for row in rows[1:-2]:
        columns = row.find_all('td')
        try:
            if not find_dict_in_list(parsed_data, f'{columns[1].getText()} Аэропорт'):
                parsed_data.append({'from':"Sheremetevo Airport", 'to':f'{columns[1].getText()} Аэропорт', 'name':'Unknown',
                                    'aircompany':'Aeroflot', 'depature_time':columns[4].getText(), 'arrival_time':columns[5].getText(),
                                    'code':columns[0].getText()})

        except IndexError:
            print('IndexError')

aircompany = Aircompany.objects.get(name__contains='Aeroflot')
airport_from = Airport.objects.get(code = 'SVO')

for row in parsed_data:
    print(row)
    try:
        to = Airport.objects.get(name__contains=f'{row["to"].split(" ")[0]}')
    except Exception as err:
        print(err)
        to = Airport.objects.create(name=row['to'], code=row['code'], location=row['to'].split()[0])

    Flight.objects.create(departure_point=airport_from, to=to, aircompany=aircompany)
    print()

print(len(parsed_data))