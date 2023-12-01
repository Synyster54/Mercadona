from django.test import TestCase, Client
from .models import Utilisateurs
from .views import connexion, deconnexion, inscription, admin
from django.urls import reverse

from django.contrib.auth import authenticate, login, logout


# Create your tests here.

class TestCaseUtilisateurs(TestCase): #test du model Utilisateurs
    def setUp(self): 
        self.data = {
            'username' : 'admin',
            "password" : 'admin'
        }

        self.user = Utilisateurs.objects.create_user(**self.data)
        self.utilisateurs = Utilisateurs.objects.get(username=self.data['username'])



    def test_Utilisateurs_username(self):
        self.assertEqual(self.utilisateurs.username,self.user.username)

    def test_Utilisateurs_password(self):
        self.assertEqual(self.utilisateurs.password,self.user.password)
        self.data['password'] = 'admin2'
        self.assertNotEqual(self.utilisateurs.password,self.data['password'])


class TestCaseInscription(TestCase): #test de la page d'inscription, recuperation de la view
    def setUp(self):
        self.client=Client()#on crée un client pour simuler les requêtes

        self.user_data = {
            'username' : 'admin',
            'password' : 'admin'
        }
        self.user = Utilisateurs.objects.create_user(**self.user_data)

    def test_InscriptionView(self): #test de la view d'inscription et les redirections
        #response = self.client.post(reverse('inscription'), self.user_data)
        #self.assertEqual(response.status_code, 200)
        #self.assertTemplateUsed(response, 'comptes/inscription.html')
        url=reverse('inscription')  #on récupère l'url de la page d'inscription
        response=self.client.get(url) #on simule une requête GET pour acceder à la page de creation de compte
        self.assertEqual(response.status_code,200)  #on vérifie que la requête a bien abouti

        data = {
            'username' : 'test',
            'password' : 'test'
        }
        response = self.client.post(url, data) #on simule une requête POST pour créer un compte
        self.assertEqual(response.status_code, 302) #on vérifie que la requête a bien abouti et la redirection 
        self.assertRedirects(response, reverse('admin')) #on vérifie que la redirection est bien vers la page admin
        self.assertTrue(Utilisateurs.objects.filter(username=data['username']).exists()) #on vérifie que le compte a bien été créé
        self.assertTrue(Utilisateurs.objects.filter(username='test').exists()) #autre facon d'ecrire la ligne du dessus

    def test_ConnexioView(self): #test de la view de connexion et les redirections
        url=reverse('connexion')
        response=self.client.get(url)
        self.assertEqual(response.status_code,200)

        response = self.client.post(url, self.user_data)#on simule une requête POST pour se connecter avec le user_data defini au debut
        self.assertEqual(response.status_code, 302) #on vérifie que la requête a bien abouti et la redirection
        self.assertRedirects(response, reverse('admin'))    #on vérifie que la redirection est bien vers la page admin
        user=Utilisateurs.objects.get(username=self.user_data['username'])
        self.assertTrue(user.is_authenticated) #on vérifie que l'utilisateur est bien connecté

    def test_DeconnexionView(self): #test de la view de deconnexion et les redirections
        self.client.login(username=self.user_data['username'], password=self.user_data['password']) #on se connecte avec le user_data defini au debut
        self.assertTrue(self.client.session['_auth_user_id'])   #on vérifie que l'utilisateur est bien connecté
        url=reverse('deconnexion')  #on récupère l'url de la page de deconnexion
        response=self.client.get(url)
        self.assertEqual(response.status_code,302) #on vérifie que la requête a bien abouti et la redirection
        self.assertRedirects(response, reverse('index'))    #on vérifie que la redirection est bien vers la page index
        #user=Utilisateurs.objects.get(username=self.user_data['username'])
        #self.assertFalse(user.is_authenticated)
        self.assertNotIn('_auth_user_id', self.client.session) #on vérifie que l'utilisateur est bien déconnecté