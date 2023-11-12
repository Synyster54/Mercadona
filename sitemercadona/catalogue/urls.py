
from django.urls import path, include
from django.contrib import admin
from . import views

#Déclaration des URL de l'application catalogue
urlpatterns = [
    path('', views.catalogue, name='catalogue'), #URL de base de l'application catalogue
    path('add_article/', views.add_article, name='add_article'), #URL de la page d'ajout d'article
    path('add_promotion/<int:id_article>/', views.add_promotion, name='add_promotion'), #URL de la page d'ajout de promotion
    ]