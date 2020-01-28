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

    page = requests.get(f'https://www.aerobilet.net/flight-search/{from_}-{to}/{date_from}/1-0-0/ALL')
    print(f'https://www.aerobilet.net/flight-search/{from_}-{to}/{date_from}/1-0-0/ALL')

    soup = BeautifulSoup(page.content, 'html.parser')

    table = soup.findAll("table", {"class": "tablesorter"})[0]
    cards = table.find_all('tr')

    parsed_data = []

    for card in cards:
        print(card)
        try:
            time_from = f'{date_from} {card.find("span", {"class": "sr-time-dep"}).getText()}'
            name = ''  # кажется, там нет номера рейса
            plane = ''  # там нет названия самолета
            time_to = f'{date_from} {card.find("span", {"class": "sr-time-arr"}).getText()}'
            aircompany = card.find("span", {"class": "airline-name-text"}).getText()

            flight_id = None

            try:
                flight_id = Flight.objects.get(departure_point=Airport.objects.get(code=from_).id,
                                               to=Airport.objects.get(code=to).id,
                                               aircompany=Aircompany.objects.get(name__contains=aircompany).id).id

                if flight_id and not Depature.objects.filter(flight=flight_id,
                                                             departure_time=time_from):  # если есть рейс, но нет вылета..

                    Depature.objects.create(name=name, plane=plane, departure_time=time_from, arrival_time=time_to,
                                            flight=flight_id)

                # parsed_data.append({'time_from': time_from.strip(), 'name': name.strip(), 'plane': plane.strip(),
                #                     'time_to': time_to.strip(), 'aircompany':aircompany.strip(), 'flight_id':flight_id})

            except:  # если нет такого рейса
                try:
                    # пробуем создать рейс и вылет
                    create_flight(departure_point=Airport.objects.get(code=from_).id,
                                          to=Airport.objects.get(code=to).id,
                                          aircompany=Aircompany.objects.get(name__contains=aircompany).id)

                    create_departure(name=name, plane=plane, departure_time=time_from, arrival_time=time_to,
                                            flight=flight_id)
                except: # если нет такой авиакомпании, тогда создаем
                    Aircompany.objects.create(name=aircompany,rating=0)

                    create_flight(departure_point=Airport.objects.get(code=from_).id,
                                          to=Airport.objects.get(code=to).id,
                                          aircompany=Aircompany.objects.get(name__contains=aircompany).id)

                    create_departure(name=name, plane=plane, departure_time=time_from, arrival_time=time_to,
                                            flight=flight_id)

        except AttributeError:
            pass


def create_flight(departure_point, to, aircompany):
    Flight.objects.create(departure_point=departure_point, to=to, aircompany=aircompany)

def create_departure(name, plane, departure_time, arrival_time, flight):
    Depature.objects.create(name=name, plane=plane, departure_time=departure_time, arrival_time=arrival_time,
                            flight=flight)