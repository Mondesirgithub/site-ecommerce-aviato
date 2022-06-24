from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms



class InscriptionForm(UserCreationForm):
	username = forms.CharField(widget=forms.TextInput({'class':'form-control'}), label="Nom d'utilisateur")
	email = forms.CharField(widget=forms.EmailInput({'class':'form-control'}), label="Email")
	password1 = forms.CharField(widget=forms.PasswordInput({'class':'form-control'}), label="Mot de passe")
	password2 = forms.CharField(widget=forms.PasswordInput({'class':'form-control'}), label="Confirmez votre mot de passe")
	photo = forms.ImageField(widget=forms.FileInput({'class':'form-control'}), label="Photo", required=False)

	class Meta(UserCreationForm.Meta):
		model = get_user_model()
		fields = ['username','email', 'password1', 'password2', 'photo']



class ConnexionForm(forms.Form):
	username = forms.CharField(required=True,widget=forms.TextInput({'class':'form-control'}), label="Nom d'utilisateur")
	password = forms.CharField(widget=forms.PasswordInput({'class':'form-control'}), label="Mot de passe")



class ModifierProfileForm(forms.ModelForm):
	username = forms.CharField(required=True,widget=forms.TextInput({'class':'form-control'}), label="Nouveau nom d'utilisateur")
	email = forms.EmailField(widget=forms.EmailInput({'class':'form-control'}), label="Nouvel email")
	photo = forms.ImageField(widget=forms.FileInput({'class':'form-control'}), label="Nouvelle photo")

	class Meta:
		model = get_user_model()
		fields = ['username','email', 'photo']