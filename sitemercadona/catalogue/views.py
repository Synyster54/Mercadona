from urllib.parse import urlencode
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Article, Promotion
from .forms import ArticleForm, PromotionForm, ArticleTriForm
from django import forms

# Create your views here.
#Definition des vues de l'application catalogue
#Definition de la vue de la page catalogue
def catalogue(request):
    catalogue = Article.objects.all() #on récupère tous les articles
    data = {'catalogue': catalogue} #on les stocke dans un dictionnaire
    if request.method == "POST": # Si on utilise la methode POST on traite les données du formulaire
        form=ArticleTriForm(request.POST) #on récupère les données du formulaire de tri
        if form.is_valid(): #on vérifie que le formulaire est valide puis on garde les infos en URL
            base_url= reverse('catalogue')
            query_string = urlencode(form.cleaned_data)
            url='{}?{}'.format(base_url, query_string)
            return redirect(url)
    else: #on traite les données de l'url
        form = ArticleTriForm()
        trier = request.GET.get('trier') # on recupere les données de l'url
        if trier == 'asc': #si on veut trier les articles par ordre croissant
            catalogue = Article.objects.order_by('libelle')
        elif trier == 'prixc': #si on veut trier les articles par prix croissant
            catalogue = Article.objects.order_by('prix')
        elif trier == 'prixd': #si on veut trier les articles par prix décroissant
            catalogue = Article.objects.order_by('-prix')
        elif trier == 'categorie': #si on veut trier les articles par catégorie
            catalogue = Article.objects.order_by('categorie')
        else: #si on ne veut pas trier les articles
            catalogue = Article.objects.all()
    return render(request, 'catalogue/catalogue.html', {'catalogue': catalogue, 'form': form}) #on retourne la page catalogue avec les articles et le formulaire de tri

#Definition de la vue de la page d'ajout d'un article
def add_article(request):
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)#on récupère les données du formulaire et le fichier image
        if form.is_valid():
            form.save()
            return redirect('admin')#on retourne sur la page admin
    else:
        form = ArticleForm()#on renvoie le formulaire
        
    return render(request, 'catalogue/add_article.html', {'form': form})

#Definition de la vue de la page d'ajout d'une promotion
def add_promotion(request, id_article):
    identifiant = get_object_or_404(Article, pk=id_article)#on récupère l'article grace à son id et on test si on le recupere bien
    if request.method == "POST":
        form = PromotionForm(request.POST)
        if form.is_valid():#Si formulaire valide, on ajoute les données dans la base de données
            pourcentage = form.cleaned_data['pourcentage']
            dateDebut = form.cleaned_data['dateDebut']
            dateFin = form.cleaned_data['dateFin']
            article_id = identifiant.pk
            Promotion.objects.create(pourcentage=pourcentage, dateDebut=dateDebut, dateFin=dateFin, article_id=identifiant.pk)
            return redirect('admin')
    else:
        form = PromotionForm()
        
    return render(request, 'catalogue/add_promotion.html', {'form': form}) 


