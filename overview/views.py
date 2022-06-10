from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Create your views here.

def index(request):
    context = {
        'title':'Moja mala strona',
    }
    return render(request,'overview/base.html',context)

def sensors(request):
    return HttpResponse("Hello world")