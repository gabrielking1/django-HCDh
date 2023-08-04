from django.shortcuts import render
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User, auth

from django.urls import reverse
from django.http import HttpResponseRedirect
# Create your views here.


def index(request):
    return render(request,'home/index.html')