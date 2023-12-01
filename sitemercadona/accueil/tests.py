from django.test import TestCase, Client
from django.urls import reverse
from .views import index
# Create your tests here.

class TestCaseAccueilView(TestCase): #test de la page d'accueil, recuperation de la view
    def setUp(self):

        self.client=Client()#on crée un client pour simuler les requêtes

    def test_AccueilView(self): #test de la view d'accueil et les redirections
        url=reverse('index')  #on récupère l'url de la page d'accueil
        response=self.client.get(url) #on simule une requête GET pour acceder à la page d'accueil
        self.assertEqual(response.status_code,200)  #on vérifie que la requête a bien abouti
        self.assertTemplateUsed(response, 'accueil/index.html') #on vérifie que le template utilisé est bien celui de la page d'accueil

