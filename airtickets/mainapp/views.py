from django.shortcuts import render

# Create your views here.

def main(request):
    return render(request, 'mainapp/index.html')

def search(request):
    return render(request, 'mainapp/search.html')
