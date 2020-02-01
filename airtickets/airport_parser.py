# coding:utf-8
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "airtickets.settings")
django.setup()

from airtickets import settings
import requests
from bs4 import BeautifulSoup
from mainapp.models import Airport
from utils import find_dict_in_list


page = requests.get('https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%BD%D0%B0%D0%B8%D0%B1%D0%BE%D0%BB%D0%B5%D0%B5_%D0%B7%D0%B0%D0%B3%D1%80%D1%83%D0%B6%D0%B5%D0%BD%D0%BD%D1%8B%D1%85_%D0%BF%D0%B0%D1%81%D1%81%D0%B0%D0%B6%D0%B8%D1%80%D1%81%D0%BA%D0%B8%D1%85_%D0%B0%D1%8D%D1%80%D0%BE%D0%BF%D0%BE%D1%80%D1%82%D0%BE%D0%B2_%D0%BC%D0%B8%D1%80%D0%B0')

soup = BeautifulSoup(page.content, 'html.parser')


tables = soup.findAll("table", {"class": "wikitable"})



parsed_data = []


table = tables[0]
for table in tables:
    body = table.find('tbody')
    rows = body.find_all('tr', recursive=False)

    for row in rows[1:61]:
        columns = row.find_all('td')
        if not find_dict_in_list(parsed_data, columns[2].getText() if not columns[2].getText().split(':')[0]=='en' else columns[1].getText()):
            parsed_data.append({'name':columns[2].getText() if not columns[2].getText().split(':')[0]=='en' else columns[1].getText(),
                                'code':columns[4].getText().split('/')[0], 'location':columns[3].getText()})

for row in parsed_data:
    print('name:', row['name'])
    print('code:', row['code'])
    print('location:', row['location'])
    if not len(Airport.objects.filter(code=row['code'])):
        Airport.objects.create(name=row['name'], code=row['code'], location=row['location'])

    print()

print(len(parsed_data))