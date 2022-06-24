from django.contrib import admin

from boutique.models import Produit,Panier,Article,CategorieProduit, ImageProduitAssociee

# Register your models here.

admin.site.register(CategorieProduit)
admin.site.register(Produit)
admin.site.register(ImageProduitAssociee)
admin.site.register(Article)
admin.site.register(Panier)
