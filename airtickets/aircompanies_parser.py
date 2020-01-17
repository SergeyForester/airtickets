# coding:utf-8
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "airtickets.settings")
django.setup()

from airtickets import settings
import requests
from bs4 import BeautifulSoup
from mainapp.models import Aircompany

page = requests.get('https://en.wikipedia.org/wiki/List_of_passenger_airlines')

soup = BeautifulSoup(page.content, 'html.parser')


tables = soup.findAll("ul")

def find_dict_in_list(list, key):
    r = ''
    try:
        r = next(item for item in list if item["name"] == key)
    except Exception as err:
        pass
    return r


parsed_data = []


c=0
for table in tables:
    rows = table.find_all('li', recursive=False)
    for row in rows:
        columns = row.find_all('a')
        if c < 1123:
            try:
                print(c)
                c+=1
                if not find_dict_in_list(parsed_data, columns[0].getText()):
                    parsed_data.append({'name':columns[0].getText()})

            except IndexError:
                print('IndexError')

for row in parsed_data:
    print('name:', row['name'])
    Aircompany.objects.create(name=row['name'], rating=0)
    print()

print(len(parsed_data))