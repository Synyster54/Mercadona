
from django.urls import path, include
from django.contrib import admin
from . import views

#Definition des urls de l'application comptes
urlpatterns = [
    path('', views.connexion, name='connexion'),#on redirige vers la page de connexion
    path('deconnexion/', views.deconnexion, name='deconnexion'),#on redirige vers la page de deconnexion
    path('inscription/', views.inscription, name='inscription'),#on redirige vers la page d'inscription
    path('admin/', views.admin, name='admin'),#on redirige vers l'espace administrateur
    ]