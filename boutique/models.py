from django.db import models
from django.conf import settings
# Create your models here.
from datetime import datetime

class CategorieProduit(models.Model):
    nom = models.CharField(max_length=50, blank=False)
    image = models.ImageField(upload_to="boutique/categoriesProduits")
    
    def __str__(self):
        return self.nom

class Produit(models.Model):
    nom = models.CharField(max_length=128, blank=False)
    prix = models.FloatField(default=0.0)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=128)
    stock = models.IntegerField(default=1)
    categorie = models.ForeignKey(CategorieProduit, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='boutique/produits', blank=True, null=True)
    
    
    def __str__(self):
        return (f"{self.nom} ({self.stock} en stock)")


class ImageProduitAssociee(models.Model):
    image = models.ImageField(upload_to="boutique/imagesProduitsAssocies")
    produit = models.ForeignKey(Produit , on_delete=models.CASCADE)

    def __str__(self):
        return self.produit.nom




class Article(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    est_commande = models.BooleanField(default=False)
    date_commande = models.DateTimeField(blank=True, null=True)
    quantite = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.produit.nom} ({self.quantite})"


class Panier(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    articles = models.ManyToManyField(Article)

    def __str__(self):
        return f"Panier pour {self.user.username}"


    def delete(self, *args, **kwargs):
        for article in self.articles.all():
            article.est_commande = True
            article.date_commande = datetime.now()
            article.save()

        self.articles.clear() #detacher les articles du panier, c'est optionnel

        super().delete(*args, **kwargs)

