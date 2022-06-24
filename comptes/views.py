from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model,login,authenticate,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .forms import InscriptionForm, ConnexionForm , ModifierProfileForm
from boutique.models import Panier

# Create your views here.

def inscription(request):
    form = InscriptionForm()
    if request.method == "POST":
        form = InscriptionForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save()
            login(request, user)
            panier, _ = Panier.objects.get_or_create(user=user)
            user.panier = panier
            print(panier)
            messages.success(request, "Le compte a été crée avec succès !!")

            return redirect('index')

    context = {
        'form':form
    }

    return render(request, 'comptes/inscription.html', context)


def connexion(request):
    form = ConnexionForm()
    message = ""
    if request.method == "POST":
        form = ConnexionForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
                messages.success(request, f"Connexion réussie !!, ravie de vous revoir Mr/Mme {user.username}")
                return redirect('index')
            else:
                message = "Username ou email incorrect !"

    context = {
        'form':form,
        'message':message
    }

    return render(request, 'comptes/connexion.html', context)



def deconnexion(request):
    logout(request)
    return render(request, 'comptes/deconnexion.html')

@login_required
def profile(request):
    panier , _= Panier.objects.get_or_create(user=request.user)
    articles = panier.articles.all()
    context = {
        'articles':articles
    }
    return render(request, "comptes/profile.html", context)


@login_required
def modifier_profile(request):
    if request.method == "POST":
        form = ModifierProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre profile a été modifié avec succès !")
            return redirect('profile')

    else:
        form = ModifierProfileForm(instance=request.user)

    context = {
        'form':form
    }

    return render(request, "comptes/modifier_profile.html", context)