import datetime

from django.http import JsonResponse
from django.shortcuts import render
from mainapp.models import Depature, Airport, Seat, Aircompany
import utils

# Create your views here.



def main(request):
    options = Airport.objects.all()

    return render(request, 'mainapp/index.html', {'options': options})


def search(request):
    from_ = request.GET['from']
    to = request.GET['to']
    date_from = request.GET['date_from']
    date_to = request.GET['date_to']

    from_ = Airport.objects.get(name=from_)
    to = Airport.objects.get(name=to)

    utils.parse_departures(from_.code, to.code, date_from)
    print(datetime.datetime.strptime(date_from, '%Y-%m-%d'))
    result = Depature.objects.filter(
                                     flight__departure_point=from_, flight__to=to)

    print(result)

    depatures_seats = []

    # for res in result:
    #     try:
    #         depatures_seats.append(Seat.objects.get(depature=res.id, is_busy=False))
    #     except:
    #         print('Exception')


    options = Airport.objects.all()

    return render(request, 'mainapp/search.html', {'result': result, 'date_from': date_from,
                                                   'date_to': date_to, 'options': options,
                                                   'depature_seats': depatures_seats})


def ajax_flight_info(request):
    flight_id = request.GET.get('flight_id', None)
    aircomapany_id = request.GET.get('aircomapany_id', None)

    aircompany = Aircompany.objects.get(id=aircomapany_id)
    depature = Depature.objects.get(flight__id=flight_id)

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
    aircompany = request.GET.get('aircomapany_id', None)
    rating = request.GET.get('rating', None)

    print(rating)

    aircompany = Aircompany.objects.get(id=aircompany)

    message = 'Возникла ошибка'

    if rating == 'up':
        aircompany.rating += 1
        message = 'Рейтинг компании был повышен'

    elif rating == 'down':
        aircompany.rating -= 1
        message = 'Рейтинг компании был понижен))'

    aircompany.save()
    data  = {
        'message':message
    }

    return JsonResponse(data)

