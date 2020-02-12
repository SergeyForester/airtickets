import datetime
import re


from mainapp.models import Flight, Airport, Aircompany, Departure


def find_dict_in_list(list, key):
    r = ''
    try:
        r = next(item for item in list if item["to"] == key)
    except Exception as err:
        pass
    return r

def get_departures(request):
    from_ = request.GET.get('from', None)
    to = request.GET.get('to', None)
    date_from = request.GET.get('date_from', None)
    date_to = request.GET.get('date_to', None)

    from_ = re.sub('[+]', ' ', from_)
    to = re.sub('[+]', ' ', to)

    print(from_)
    print(to)
    print(date_from)
    print(date_to)

    from_ = Airport.objects.get(name=from_)
    to = Airport.objects.get(name=to)

    result = Departure.objects.filter(depature_time__date=datetime.datetime.strptime(date_from, '%Y-%m-%d'),
                                     flight__departure_point=from_,
                                     flight__to=to)

    return result
