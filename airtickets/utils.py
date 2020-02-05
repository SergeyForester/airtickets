import datetime
import re

import requests
import random

from bs4 import BeautifulSoup

from mainapp.models import Flight, Airport, Aircompany, Depature


def find_dict_in_list(list, key):
    r = ''
    try:
        r = next(item for item in list if item["to"] == key)
    except Exception as err:
        pass
    return r


def parse_departures(from_, to, date_from):
    print(from_, to, date_from)

    page = requests.get(f'https://www.aerobilet.net/flight-search/{from_}-{to}/{date_from}/1-0-0/ALL',
                        )
    print(f'https://www.aerobilet.net/flight-search/{from_}-{to}/{date_from}/1-0-0/ALL')

    soup = BeautifulSoup(page.content, 'html.parser')

    table = soup.findAll("table", {"class": "tablesorter"})[0]
    cards = table.find_all('tr')

    parsed_data = []

    for card in cards:
        try:
            time_from = f'{date_from} {card.find("span", {"class": "sr-time-dep"}).getText()}'
            name = ''  # кажется, там нет номера рейса
            plane = ''  # там нет названия самолета
            time_to = re.sub('[()]', '', f'{date_from} {card.find("span", {"class": "sr-time-arr"}).getText()}')
            aircompany = card.find("span", {"class": "airline-name-text"}).getText()


            try:
                flight = Flight.objects.filter(departure_point=Airport.objects.get(code=from_),
                                                  to=Airport.objects.get(code=to),
                                                  aircompany=Aircompany.objects.get(name__contains=aircompany))[0]
            except:
                flight = None

            if flight and not len(Depature.objects.filter(flight=flight,
                depature_time=time_from)):  # если есть рейс, но нет вылета..

                Depature.objects.create(name=name, plane=plane, depature_time=time_from, arrival_time=time_to,
                                        flight=flight)

            # parsed_data.append({'time_from': time_from.strip(), 'name': name.strip(), 'plane': plane.strip(),
            #                     'time_to': time_to.strip(), 'aircompany':aircompany.strip(), 'flight_id':flight_id})

            if not flight:  # если нет такого рейса
                try:
                    # пробуем создать рейс и вылет
                    print(Airport.objects.get(code=from_).id)
                    print(Airport.objects.get(code=to).id)
                    print(Aircompany.objects.get(name__contains=aircompany).id)

                    Flight.objects.create(departure_point=Airport.objects.get(code=from_),
                                  to=Airport.objects.get(code=to),
                                  aircompany=Aircompany.objects.get(name__contains=aircompany))

                    Depature.objects.create(name=name, plane=plane, depature_time=time_from, arrival_time=time_to,
                                     flight=flight)

                except Exception as err:  # если нет такой авиакомпании, тогда создаем
                    Aircompany.objects.create(name=aircompany, rating=0)

                    Flight.objects.create(departure_point=Airport.objects.get(code=from_).id,
                                  to=Airport.objects.get(code=to).id,
                                  aircompany=Aircompany.objects.get(name__contains=aircompany).id)

                    Depature.objects.create(name=name, plane=plane, depature_time=time_from, arrival_time=time_to,
                                     flight=flight)


        except Exception as err:
            print('AttributeError', err)
    print()


def create_flight(departure_point, to, aircompany):
    Flight.objects.create(departure_point=int(departure_point), to=int(to), aircompany=int(aircompany))


def create_departure(name, plane, departure_time, arrival_time, flight):
    Depature.objects.create(name=name, plane=plane, depature_time=departure_time, arrival_time=arrival_time,
                            flight=flight)
