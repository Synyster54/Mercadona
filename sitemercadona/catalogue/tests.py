from django.test import TestCase, Client
from .models import Article, Promotion
from .forms import ArticleForm
from django.urls import reverse
from .views import catalogue, add_article, add_promotion
import datetime

# Create your tests here.

class TestCaseArticle(TestCase): #test du model Article par la création d'un article
    def setUp(self):
        self.data = {
            'libelle' : 'test',
            'description' : 'test',
            'prix' : 10.00,
            'image' : 'test',
            'categorie' : 'test'
        }
        self.article = Article.objects.create(**self.data)
        self.article = Article.objects.get(libelle=self.data['libelle'])
        
    def test_Article_libelle(self):
        self.assertEqual(self.article.libelle,self.data['libelle'])
        
    def test_Article_description(self):
        self.assertEqual(self.article.description,self.data['description'])
        
    def test_Article_prix(self):
        self.assertEqual(self.article.prix,self.data['prix'])
        
    def test_Article_image(self):
        self.assertEqual(self.article.image,self.data['image'])
        
    def test_Article_categorie(self):
        self.assertEqual(self.article.categorie,self.data['categorie']) 


class TestCaseFormArticle(TestCase): #test du formulaire de création d'article
    def setUp(self):
        self.data = {
            'libelle' : 'test',
            'description' : 'test',
            'prix' : 10.00,
            'image' : 'test',
            'categorie' : 'test'
        }
        self.article = Article.objects.create(**self.data)
        self.article = Article.objects.get(libelle=self.data['libelle'])

    def test_ArticleForm(self):
        form = ArticleForm(data=self.data) #création du formulaire avec les données
        self.assertTrue(form.is_valid()) #vérification de la validité du formulaire
    
class TestCaseCatalogueView(TestCase): #test de la page du catalogue, recuperation de la view
    def setUp(self):

        self.client=Client()#on crée un client pour simuler les requêtes

        self.article_data = { #on crée un dictionnaire avec les données de l'article
            'libelle' : 'test',
            'description' : 'test',
            'prix' : 10.00,
            'image' : 'test',
            'categorie' : 'test'
        }
        self.article = Article.objects.create(**self.article_data)
    
    def test_CatalogueView(self): #test de la view du catalogue
        url=reverse('catalogue')  #on récupère l'url de la page du catalogue
        response=self.client.get(url) #on simule une requête GET pour acceder à la page du catalogue
        self.assertEqual(response.status_code,200)  #on vérifie que la requête a bien abouti
        self.assertTemplateUsed(response, 'catalogue/catalogue.html') #on vérifie que le template utilisé est bien le bon
        self.assertTrue(Article.objects.filter(libelle=self.article_data['libelle']).exists()) #on vérifie que l'article a bien été créé
        self.assertTrue(Article.objects.filter(libelle='test').exists()) #autre facon d'ecrire la ligne du dessus


    def test_CatalogueAddArticleView(self): #test de la view d'ajout d'article
        url=reverse('add_article') #on récupère l'url de la page d'ajout d'article
        response=self.client.get(url) #on simule une requête GET pour acceder à la page d'ajout d'article
        self.assertEqual(response.status_code,200)  #on vérifie que la requête a bien abouti
        
        response = self.client.post(url, self.article_data)#on simule une requête POST pour ajouter un article avec les données de l'article defini au debut
        self.assertEqual(response.status_code, 302) #on vérifie que la requête a bien abouti et la redirection
        self.assertRedirects(response, reverse('admin')) #on vérifie que la redirection est bien vers la page admin
        self.assertTrue(Article.objects.filter(libelle=self.article_data['libelle']).exists()) #on vérifie que l'article a bien été créé

    def test_CatalogueAddPromotionView(self): #test de la view d'ajout de promotion
        url=reverse('add_promotion', args=[self.article.pk]) #on récupère l'url de la page d'ajout de promotion en mettant en argument l'article créé au début
        response=self.client.get(url) #on simule une requête GET pour acceder à la page d'ajout de promotion
        self.assertEqual(response.status_code,200)  #on vérifie que la requête a bien abouti
        
        data = { #on crée un dictionnaire avec les données de la promotion
            'pourcentage' : 10,
            'dateDebut' : '2020-01-01',
            'dateFin' : '2020-01-02',
        }
        response = self.client.post(url, data) #on simule une requête POST pour ajouter une promotion avec les données de la promotion defini au debut
        self.assertEqual(response.status_code, 302) #on vérifie que la requête a bien abouti et la redirection
        self.assertRedirects(response, reverse('admin')) #on vérifie que la redirection est bien vers la page admin
        self.assertTrue(Promotion.objects.filter(pourcentage=data['pourcentage']).exists()) #on vérifie que la promotion a bien été créé

class TestCasePromoArticle(TestCase):
    def setUp(self):
        self.article_data = {   #on crée un dictionnaire avec les données de l'article
            'libelle' : 'test',
            'description' : 'test',
            'prix' : 10.00,
            'image' : 'test',
            'categorie' : 'test'
        }
        self.article = Article.objects.create(**self.article_data) #on crée l'article
        self.article = Article.objects.get(libelle=self.article_data['libelle']) #on récupère l'article créé
        
        self.promotion_data = { #on crée un dictionnaire avec les données de la promotion
            'pourcentage' : 10,
            'dateDebut' : datetime.date.today(),
            'dateFin' : datetime.date.today(),
            'article' : self.article
        }
        self.promotion = Promotion.objects.create(**self.promotion_data)
        self.promotion = Promotion.objects.get(pourcentage=self.promotion_data['pourcentage'])
        
    def test_PromoArticle(self):
        self.assertEqual(self.article.promo_article(),9.00) #on vérifie que le prix de l'article est bien de 9.00 avec la promotion

    def test_PromoArticleNoPromo(self):
        self.promotion.delete() #on supprime la promotion
        self.assertEqual(self.article.promo_article(),10.00) #on vérifie que le prix de l'article est bien de 10.00 sans promotion

    def test_PromoArticleNoPromoDate(self):
        self.promotion.dateDebut = '2020-01-02' #on change la date de début de la promotion
        self.promotion.dateFin = '2020-01-03' #on change la date de fin de la promotion
        self.promotion.save() #on sauvegarde la promotion
        self.assertEqual(self.article.promo_article(),10.00) #on vérifie que le prix de l'article est bien de 10.00 sans promotion

    def test_PromoArticleNoPromoDate2(self):
        self.promotion.dateDebut = datetime.date.today() #on change la date de début de la promotion
        self.promotion.dateFin = datetime.date.today() #on change la date de fin de la promotion
        self.promotion.save() #on sauvegarde la promotion
        self.assertEqual(self.article.promo_article(),9.00) #on vérifie que le prix de l'article est bien de 9.00 avec la