from django.contrib import admin
from mainapp.models import Airport, Aircompany, Flight, Depature
# Register your models here.
admin.site.register(Airport)
admin.site.register(Aircompany)
admin.site.register(Flight)
admin.site.register(Depature)