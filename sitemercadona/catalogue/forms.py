from django.forms import ModelForm
from django import forms
from .models import Article, Promotion

# Declaration du formulaire de creation d'article depuis le model Article
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('libelle', 'description', 'prix', 'categorie', 'image')#choix des champs du formulaire à saisir par l'utilisateur
    
# Declaration du formulaire de creation de promotion depuis le model Promotion
class PromotionForm(forms.ModelForm):
    class Meta:
        model = Promotion
        fields = ('pourcentage', 'dateDebut', 'dateFin')#choix des champs du formulaire à saisir par l'utilisateur

# Declaration du formulaire de tri d'article
class ArticleTriForm(forms.Form):
    # Declaration des choix de tri possible
    choix = (('','Choisir un tri'),('asc', 'Ordre Alphabétique'), ('prixc', 'Prix croissant'), ('prixd', 'Prix décroissant'), ('categorie', 'Catégorie'))
    trier = forms.ChoiceField(choices=choix)#création du formulaire de type liste déroulante