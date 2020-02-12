from django.contrib import admin
from mainapp.models import Airport, Aircompany, Flight, Departure, Seat, SeatType
# Register your models here.
admin.site.register(Airport)
admin.site.register(Aircompany)
admin.site.register(Flight)
admin.site.register(Departure)
admin.site.register(Seat)
admin.site.register(SeatType)