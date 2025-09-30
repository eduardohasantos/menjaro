from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("Created first APP")
# Create your views here.
