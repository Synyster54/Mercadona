from django.shortcuts import render
from django.http import HttpResponse


# Definition de la vue index, qui renvoie la page d'accueil et au fichier index.html
def index(request):
    return render(request, 'accueil/index.html', {'index':index})