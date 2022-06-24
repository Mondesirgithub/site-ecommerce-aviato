from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib import messages
from boutique.models import Produit, Article, Panier,CategorieProduit
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
# Create your views here.


def index(request):
    produits = Produit.objects.all()
    if not request.user.is_anonymous:
        panier, _ = Panier.objects.get_or_create(user=request.user)

    categories = CategorieProduit.objects.all()
    context = {
        'produits':produits,
        'categoriesProduit':categories
    }
    
    return render(request, 'boutique/index.html', context)


def details_produit(request, slug):
    produit = get_object_or_404(Produit,slug=slug)
    images_associees_produit = produit.imageproduitassociee_set.all()
    if not request.user.is_anonymous:
        panier, _ = Panier.objects.get_or_create(user=request.user)

    context = {
        'produit':produit,
        'images_associees_produit':images_associees_produit
    }
    return render(request, 'boutique/details_produit.html', context)


@login_required
def ajouter_au_panier(request, slug):
    panier, _ = Panier.objects.get_or_create(user=request.user)

    if request.method == "POST":
        quantite = int(request.POST['product-quantity'])
        produit = get_object_or_404(Produit, slug=slug)
        user = request.user
        panier, _ = Panier.objects.get_or_create(user=user)
        article, article_cree = Article.objects.get_or_create(user=user,est_commande=False,produit=produit)

        if quantite == 0:
            messages.error(request, "Veuillez entrer une quantité supérieure à 0")

        else:
            if (article.produit.stock - quantite) >= 0:
                if article_cree:
                    article.quantite = quantite
                    article.save()
                    panier.articles.add(article)
                    panier.save()

                else:
                    article.quantite+=quantite
                    article.save()
                    panier.save()

                messages.success(request, f"Ajout de {quantite} {article.produit.nom}(s) dans le panier réussi !")

            else:
               messages.error(request, "Stock insuffisant")

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
   


@login_required
def panier(request):
    panier, _ = Panier.objects.get_or_create(user=request.user)
    articles = panier.articles.all()

    total = 0
    for article in articles:
        total += (article.produit.prix * article.quantite)

    context = {
        'articles':articles,
        'total':total
    }

    return render(request, 'boutique/panier.html', context)


@login_required
def vider_panier(request):
    panier, _ = Panier.objects.get_or_create(user=request.user)
    articles = panier.articles.all()
    articles.delete()
    context = {
        'articles':articles
    }
    messages.success(request, "Votre panier a été vidé avec succès !")
    return render(request, "boutique/panier.html", context)


def boutique(request):
    produits = Produit.objects.all()
    if not request.user.is_anonymous:
        panier, _ = Panier.objects.get_or_create(user=request.user)

    categories = CategorieProduit.objects.all()
    context = {
        'produits':produits,
        'categories':categories
    }
    
    return render(request, 'boutique/boutique.html', context)



def produits_categorie(request, id):
    categorie = get_object_or_404(CategorieProduit, id=id)
    if not request.user.is_anonymous:
        panier, _ = Panier.objects.get_or_create(user=request.user)

    produits = categorie.produit_set.all()

    context = {
        'produits_categorie':produits,
        'categorie':categorie
    }

    return render(request, "boutique/produits_categorie.html", context)


def traitementDeLaRecherche(request):
    if not request.user.is_anonymous:
        panier, _ = Panier.objects.get_or_create(user=request.user)

    categories = CategorieProduit.objects.all()
    context = {
        'categories':categories
    }
    if request.method == "POST":
        if request.POST['nom'] != "":
            nom = request.POST['nom']
            produits = Produit.objects.filter(nom__icontains=nom)
            if len(produits) == 0:
                messages.info(request, f"0 produit trouvé correspondant à <<{nom}>>, saisissez un autre nom")

            else:
                messages.info(request, f"{len(produits)} produit(s) trouvé(s) correspondant à <<{nom}>>")
            
            context['produits'] = produits

        elif request.POST['prixmin'] != "" and request.POST['prixmax'] != "":
            prixmin = float(request.POST['prixmin'])
            prixmax = float(request.POST['prixmax'])
            if prixmin > prixmax:
                messages.error(request,"Le prix minimal doit être inférieur au prix maximal")
                context['produits'] = []
            
            elif prixmin == prixmax:
                produits = Produit.objects.filter(prix=prixmin)
                messages.info(request, f"{len(produits)} produit(s) trouvé(s) ayant le prix de <<{prixmin} FCFA>>")
                context['produits'] = produits

            else:
                produits = Produit.objects.filter(prix__range=(prixmin, prixmax))
                messages.info(request, f"{len(produits)} produit(s) trouvé(s) ayant un prix entre <<{prixmin} FCFA>> et <<{prixmax} FCFA>>")
                context['produits'] = produits

        elif request.POST['categorie'] != "":
            categorie_nom = request.POST['categorie']
            categorie = get_object_or_404(CategorieProduit, nom=categorie_nom)
            produits = Produit.objects.filter(categorie=categorie)
            messages.info(request, f"{len(produits)} produit(s) trouvé(s) faisant parti de la categorie <<{categorie_nom}>>")
            context['produits'] = produits

    return render(request, "boutique/boutique.html", context)



@login_required
def paiement(request):
    panier, _ = Panier.objects.get_or_create(user=request.user)
    articles = panier.articles.all()
    if len(articles) == 0:
        return redirect('panier')
    else:
        total = 0
        for article in articles:
            total += (article.produit.prix * article.quantite)

        context = {
            'articles':articles,
            'total':total
        }

    if request.method == "POST":
        for article in articles:    
            article.produit.stock -= article.quantite
            article.produit.save()

        request.user.panier.delete()
        return redirect('confirmation_paiement')        

    return render(request, "boutique/paiement.html", context)


@login_required
def confirmation_paiement(request):
    panier, _ = Panier.objects.get_or_create(user=request.user)
    articles = panier.articles.all()
    articles = []
    return render(request, "boutique/confirmation_paiement.html")



@login_required
def historique_commandes(request):
    articles = Article.objects.filter(est_commande=True, user=request.user)
    if not request.user.is_anonymous:
        panier, _ = Panier.objects.get_or_create(user=request.user)
        
    context = {
        'articles':articles
    }

    return render(request, "boutique/historique_commandes.html", context)



def mise_a_jour(request):
    articles = panier.articles.all()
    if not request.user.is_anonymous:
        panier, _ = Panier.objects.get_or_create(user=request.user)
        
    if request.method == "POST":
        i = 1
        for article in articles:
            quantite = int(request.POST[f'product-quantity{i}'])

            if quantite > article.produit.stock:
                messages.error(request, f"Stock insuffisant")  

            else:
                if article.quantite > quantite:
                    nombre = article.quantite - quantite
                    messages.success(request, f"Mise à jour du panier réussi, {nombre} {article.produit.nom}(s) ont été retiré(s)")
                    article.quantite = quantite

                elif article.quantite < quantite:
                    nombre = quantite - article.quantite
                    messages.success(request, f"Mise à jour du panier réussi, {nombre} {article.produit.nom}(s) ont été rajouté(s)")
                    article.quantite = quantite

                article.save()


                if article.quantite == 0:
                    article.delete()
                    messages.success(request, "L'article a été retiré du panier ")

            i += 1

    return redirect("panier")



def handle_not_found(request,exception):
    
    return render(request, "boutique/404.html")