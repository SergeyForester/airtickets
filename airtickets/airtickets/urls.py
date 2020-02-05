"""airtickets URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import mainapp.views as mainapp

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', mainapp.main, name='main'),
    path('search', mainapp.search, name='search'),
    path('ajax/flight_info', mainapp.ajax_flight_info, name="ajax_flight_info"),
    path('ajax/aircompany_rating', mainapp.ajax_aircompany_rating, name="ajax_aircompany_rating"),
    path('ajax/departures_scrapper', mainapp.ajax_departures_scrapper, name="ajax_departures_scrapper"),
]


from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)