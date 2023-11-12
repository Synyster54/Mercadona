from django.db import models
from django.shortcuts import render

# Create your models here.
#Definition des models de l'application catalogue pour la base de données POSTGRESQL
class Article(models.Model):
    libelle = models.CharField(max_length=50) #nom de l'article
    description = models.TextField() #Description de l'article
    prix = models.DecimalField(max_digits=10, decimal_places=2) #Prix de l'article en floatant à deux chiffres après la virgule
    image = models.ImageField(upload_to="img/", null=True, blank=True) #Image de l'article avec chemin de stockage
    categorie = models.CharField(max_length=50) #Catégorie de l'article

    def promo_article(self): #Fonction de calcul du prix de l'article en fonction de la promotion
        import datetime
        article=Article.objects.get(pk=self.pk) #Récupération de l'article
        try: #oon essaie de recuperer la promotion de l'article si il y en a une
            promo=Promotion.objects.get(article_id=article.pk) #Récupération de la promotion de l'article grace à la clé étrangère
            date_jour = datetime.date.today() #on recupere la date du jour
            if promo.dateDebut <= date_jour <= promo.dateFin: #on verifie si la promotion est en cours
                reduction = float(article.prix) * ((100-promo.pourcentage) / 100) #calcule du prix promotionnel
                return round(reduction,2) #on retourne le prix promotionnel arrondi à deux chiffres après la virgule
            return article.prix #si la promotion n'est pas en cours on retourne le prix normal
        except:
            return article.prix #si il n'y a pas de promotion on retourne le prix normal
        
    def __str__(self):
        return f"{self.pk}({self.libelle})" #on retourne l'id et le libelle de l'article
    
#Definition du model promotion pour la base de données POSTGRESQL     
class Promotion(models.Model):
    pourcentage = models.IntegerField()
    dateDebut = models.DateField()
    dateFin = models.DateField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE) #clé étrangère de l'article

    def __str__(self):
        return self.article.libelle

