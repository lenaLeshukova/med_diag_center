from django.shortcuts import render
from django.urls import path

app_name = 'appointments'

urlpatterns = [
    path('login/', lambda r: render(r, 'base.html'), name='login'),
    path('register/', lambda r: render(r, 'base.html'), name='register'),
    path('logout/', lambda r: render(r, 'base.html'), name='logout'),
    path('dashboard/', lambda r: render(r, 'base.html'), name='dashboard'),
]
