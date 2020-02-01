# coding:utf-8
import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "airtickets.settings")
django.setup()

from airtickets import settings
import requests
from bs4 import BeautifulSoup
from mainapp.models import Aircompany
from utils import find_dict_in_list

page = requests.get('https://en.wikipedia.org/wiki/List_of_passenger_airlines')

soup = BeautifulSoup(page.content, 'html.parser')

tables = soup.findAll("ul")

parsed_data = []

count = 0
for table in tables:
    rows = table.find_all('li', recursive=False)
    for row in rows:
        columns = row.find_all('a')
        if count < 1123:  # дальше парсить нельзя (там не нужные данные)
            try:
                print(count)
                count += 1
                if not find_dict_in_list(parsed_data, columns[0].getText()):
                    parsed_data.append({'name': columns[0].getText()})

            except IndexError:
                print('IndexError')

for row in parsed_data:
    print('name:', row['name'])
    Aircompany.objects.create(name=row['name'], rating=0)
    print()

print(len(parsed_data))
