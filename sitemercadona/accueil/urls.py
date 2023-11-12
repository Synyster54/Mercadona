
from django.urls import path
from . import views

#declaration de l'URL de la page d'accueil, qui arrive sur la vue index
urlpatterns = [
    path('', views.index, name='index'),
    ]