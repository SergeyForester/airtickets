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
            print('parsing..')
            time_from = f'{date_from} {card.find("span", {"class": "sr-time-dep"}).getText()}'
            name = ''  # кажется, там нет номера рейса
            plane = ''  # там нет названия самолета
            time_to = re.sub('[()]', '', f'{date_from} {card.find("span", {"class": "sr-time-arr"}).getText()}')
            aircompany = card.find("span", {"class": "airline-name-text"}).getText()
            print(time_from, name, plane, time_to, aircompany)


            try:
                flight_id = Flight.objects.filter(departure_point=Airport.objects.get(code=from_).id,
                                                  to=Airport.objects.get(code=to).id,
                                                  aircompany=Aircompany.objects.get(name__contains=aircompany).id)[0].id
            except:
                flight_id = None

            print('flight_id',flight_id)

            if flight_id and not len(Depature.objects.filter(flight=flight_id,
                                                         departure_time=time_from)):  # если есть рейс, но нет вылета..

                create_departure(name=name, plane=plane, departure_time=time_from, arrival_time=time_to,
                                        flight=flight_id)
                print('Departure creating, flight exists')
            # parsed_data.append({'time_from': time_from.strip(), 'name': name.strip(), 'plane': plane.strip(),
            #                     'time_to': time_to.strip(), 'aircompany':aircompany.strip(), 'flight_id':flight_id})

            if not flight_id:  # если нет такого рейса
                print('trying create flight and departure')
                try:
                    # пробуем создать рейс и вылет
                    print(Airport.objects.get(code=from_).id)
                    print(Airport.objects.get(code=to).id)
                    print(Aircompany.objects.get(name__contains=aircompany).id)

                    Flight.objects.create(departure_point=Airport.objects.get(code=from_).id,
                                  to=Airport.objects.get(code=to).id,
                                  aircompany=Aircompany.objects.get(name__contains=aircompany).id)

                    Depature.objects.create(name=name, plane=plane, departure_time=time_from, arrival_time=time_to,
                                     flight=flight_id)
                    print('flight and departure have been created')

                except Exception as err:  # если нет такой авиакомпании, тогда создаем
                    print('ERR', err)
                    print('trying to create aircompany')
                    Aircompany.objects.create(name=aircompany, rating=0)

                    Flight.objects.create(departure_point=Airport.objects.get(code=from_).id,
                                  to=Airport.objects.get(code=to).id,
                                  aircompany=Aircompany.objects.get(name__contains=aircompany).id)

                    Depature.objects.create(name=name, plane=plane, departure_time=time_from, arrival_time=time_to,
                                     flight=flight_id)

                    print('flight and departure and aircompany have been created')

        except Exception as err:
            print('AttributeError', err)
    print()


def create_flight(departure_point, to, aircompany):
    Flight.objects.create(departure_point=int(departure_point), to=int(to), aircompany=int(aircompany))


def create_departure(name, plane, departure_time, arrival_time, flight):
    Depature.objects.create(name=name, plane=plane, departure_time=departure_time, arrival_time=arrival_time,
                            flight=flight)
