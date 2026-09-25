from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('', views.catalog_view, name='catalog'),
]
