from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from . import models

def home(request):
    return render(request, 'home.html')
