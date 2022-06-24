from django.urls import path
from boutique.views import (index, boutique,details_produit,
 ajouter_au_panier, 
 panier,
 vider_panier,
 paiement,
 mise_a_jour,
 confirmation_paiement,
 historique_commandes,
 produits_categorie, traitementDeLaRecherche)
from django.contrib.auth import views


urlpatterns = [
    path('', index, name='index'),
    path('boutique', boutique, name='boutique'),
    path('details_produit/<str:slug>', details_produit, name='details_produit'),
    path('ajouter_au_panier/<str:slug>', ajouter_au_panier, name='ajouter_au_panier'),
    path('produits_categorie/<int:id>', produits_categorie, name='produits_categorie'),
    path('recherche/', traitementDeLaRecherche , name='traitementDeLaRecherche'),
    path('vider_panier/', vider_panier, name='vider_panier'),
    path('panier/', panier, name='panier'),
    path('mise_a_jour/', mise_a_jour, name='mise_a_jour'),
    path('paiement/', paiement, name='paiement'),
    path('historique_commandes/', historique_commandes, name='historique_commandes'),
    path('confirmation_paiement/', confirmation_paiement, name='confirmation_paiement'),
]
