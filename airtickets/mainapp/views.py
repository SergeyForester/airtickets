import datetime
import re

from django.http import JsonResponse
from django.shortcuts import render
from mainapp.models import Depature, Airport, Seat, Aircompany
import parsers
import utils


# Create your views here.


def main(request):
    options = Airport.objects.all()

    return render(request, 'mainapp/index.html', {'options': options})


def search(request):
    options = Airport.objects.all()

    return render(request, 'mainapp/search.html', {'options': options})


def ajax_departures_scrapper(request):
    from_ = request.GET.get('from', None)
    to = request.GET.get('to', None)
    date_from = request.GET.get('date_from', None)

    from_ = re.sub('[+]', ' ', from_)
    to = re.sub('[+]', ' ', to)

    from_ = Airport.objects.get(name=from_)
    to = Airport.objects.get(name=to)

    parsers.parse_departures(from_.code, to.code, date_from)

    result = utils.get_departures(request)

    data = {
        'departures': [{'departure_id': departure.id,
                        'aircompany_id': departure.flight.aircompany.id,
                        'aircompany_name': departure.flight.aircompany.name,
                        'departure_time': departure.depature_time.strftime("%H:%M"),
                        'departure_point_name': departure.flight.departure_point.name,
                        'departure_date': departure.depature_time.strftime("%Y-%m-%d"),
                        'name': departure.name,
                        'aircomany_rating': departure.flight.aircompany.rating,
                        'arrival_time': departure.arrival_time.strftime("%H:%M"),
                        'arrival_point_name': departure.flight.to.name,
                        'arrival_date': departure.arrival_time.strftime("%Y-%m-%d")}
                       for departure in result]
    }

    return JsonResponse(data)


def ajax_flight_info(request):
    departure_id = request.GET.get('departure_id', None)
    aircomapany_id = request.GET.get('aircompany_id', None)

    print(departure_id)
    print(aircomapany_id)

    aircompany = Aircompany.objects.get(id=aircomapany_id)
    depature = Depature.objects.get(id=departure_id)

    data = {
        'aircompany': aircompany.name,
        'aircompany_rating': aircompany.rating,
        'flight_code': depature.name,
        'from': depature.flight.departure_point.name,
        'to': depature.flight.to.name,
        'date_from': depature.depature_time,
        'date_to': depature.arrival_time,
        'aircompany_description': aircompany.description
    }

    return JsonResponse(data)


def ajax_aircompany_rating(request):
    aircompany = request.GET.get('aircompany_id', None)
    rating = request.GET.get('rating', None)

    print(rating)
    print(aircompany)

    aircompany = Aircompany.objects.get(id=aircompany)

    message = 'Возникла ошибка'

    if rating == 'up':
        aircompany.rating += 1
        message = 'Рейтинг компании был повышен'

    elif rating == 'down':
        if aircompany.rating != 0:
            aircompany.rating -= 1
            message = 'Рейтинг компании был понижен))'
        else:
            message = 'Рейтинг компании равен нулю'

    aircompany.save()
    data = {
        'message': message
    }

    return JsonResponse(data)


def ajax_results_filter(request):
    key = request.GET.get('filter_key', None)

    result = utils.get_departures(request)

    if key == 'filter-departure-time-earliest':
        result = sorted(result, key=lambda k: k.depature_time)
    elif key == 'filter-departure-time-latest':
        result = sorted(result, key=lambda k: k.depature_time, reverse=True)

    elif key == 'filter-company-rating-descending':
        result = sorted(result, key=lambda k: k.flight.aircompany.rating, reverse=True)
    elif key == 'filter-company-rating-ascending':
        result = sorted(result, key=lambda k: k.flight.aircompany.rating)

    elif key == 'filter-flight-time-descending':
        result = sorted(result,
                        key=lambda k: k.depature_time - k.arrival_time,
                        reverse=True)
    elif key == 'filter-flight-time-ascending':
        result = sorted(result,
                        key=lambda k: k.depature_time - k.arrival_time)
    else:
        print('UNKNOWN FILTER KEY')

    data = {
        'departures': [{'departure_id': departure.id,
                        'aircompany_id': departure.flight.aircompany.id,
                        'aircompany_name': departure.flight.aircompany.name,
                        'departure_time': departure.depature_time.strftime("%H:%M"),
                        'departure_point_name': departure.flight.departure_point.name,
                        'departure_date': departure.depature_time.strftime("%Y-%m-%d"),
                        'name': departure.name,
                        'aircomany_rating': departure.flight.aircompany.rating,
                        'arrival_time': departure.arrival_time.strftime("%H:%M"),
                        'arrival_point_name': departure.flight.to.name,
                        'arrival_date': departure.arrival_time.strftime("%Y-%m-%d")}
                       for departure in result]
    }

    return JsonResponse(data)
