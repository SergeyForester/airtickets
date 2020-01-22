import datetime

from django.shortcuts import render
from mainapp.models import Depature, Airport


# Create your views here.

def main(request):
    options = Airport.objects.all()

    return render(request, 'mainapp/index.html', {'options': options})


def search(request):
    from_ = request.GET['from']
    to = request.GET['to']
    date_from = request.GET['date_from']
    date_to = request.GET['date_to']

    from_ = Airport.objects.get(name=from_).id
    to = Airport.objects.get(name=to).id

    result = Depature.objects.filter(depature_time__date=datetime.datetime.strptime(date_from, '%Y-%m-%d'),
                                     flight__departure_point=from_, flight__to=to)

    options = Airport.objects.all()

    return render(request, 'mainapp/search.html', {'result': result, 'date_from':date_from,
                                                   'date_to':date_to, 'options':options})
