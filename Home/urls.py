from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# app_name = 'Myapp'
urlpatterns = [
        path('',views.index, name='index'),
]