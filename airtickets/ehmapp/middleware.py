#coding:utf-8
import mainapp.views as mainapp
from django.http import HttpResponseServerError
from django.template import loader


class ExceptionHandlerMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        print(response)

        if response.status_code == 404:
            print(response.status_code)
            mainapp.handler404(request, 404)

        if response.status_code == 500:
            print(response.status_code)
            template = loader.get_template('mainapp/502.html')
            return HttpResponseServerError(template.render())

        return response