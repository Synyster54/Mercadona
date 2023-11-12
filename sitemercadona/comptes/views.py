from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import Utilisateurs
from django import forms
from django.contrib.auth import authenticate, login, logout


# Create your views here.
#Definition des vues de l'application comptes
#Vue Connexion
def connexion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)#on verifie si l'utilisateur existe
        if user is not None:#si l'utilisateur existe on le connecte
            login(request, user)
            return redirect('admin')#on redirige vers l'espace administrateur
        else:
            return HttpResponse("Erreur de connexion")#sinon on affiche un message d'erreur
    return render(request, 'comptes/connexion.html', {'connexion':connexion})

#Vue Deconnexion
def deconnexion(request):#on deconnecte l'utilisateur lors du clique sur le bouton de deconnexion
    logout(request)
    return redirect('index')

#Vue Inscription d'un nouvel administrateur
def inscription(request):
    if request.method == 'POST': #Si on utilise la methode POST on traite les données du formulaire
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=Utilisateurs.objects.create_user(username=username, password=password)#on crée un nouvel utilisateur
        login(request, user)#on le connecte en même temps
        return redirect('admin')#on redirige vers l'espace administrateur
    return render(request, 'comptes/inscription.html', {'inscription':inscription})

#Vue Espace Administrateur
def admin(request):
    return render(request, 'comptes/admin.html', {'admin':admin})