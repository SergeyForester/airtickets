import datetime

from django.shortcuts import render
from mainapp.models import Depature, Airport


# Create your views here.

def main(request):
    options = Airport.objects.all()

    return render(request, 'mainapp/index.html', {'options':options})


def search(request):
    from_ = request.GET['from']
    to = request.GET['to']
    date_from = request.GET['date_from']
    date_to = request.GET['date_to']

    print(from_, type(from_))
    print(to, type(to))
    print(date_from, type(date_from))
    print(date_to, type(date_to))

    result = Depature.objects.filter(depature_time__date=datetime.datetime.strptime(date_from, '%Y-%m-%d'),
                                      flight__departure_point = from_, flight__to = to )

    return render(request, 'mainapp/search.html', {'result':result})
