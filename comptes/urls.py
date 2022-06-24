from django.urls import path
from comptes.views import inscription,connexion, deconnexion, profile, modifier_profile
from django.contrib.auth import views


urlpatterns = [
    path('inscription/', inscription, name='inscription'),
    path('connexion/', connexion, name='connexion'),
    path('deconnexion/', deconnexion, name='deconnexion'),
    path('modifier_profile/', modifier_profile, name='modifier_profile'),
    path('profile/', profile, name='profile'),
    path('reset_password/', views.PasswordResetView.as_view(template_name="comptes/password_reset.html"), name='password_reset'),
    path('reset_password_sent/', views.PasswordResetDoneView.as_view(template_name="comptes/password_reset_done.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>', views.PasswordResetConfirmView.as_view(template_name="comptes/password_reset_form.html"), name='password_reset_confirm'),
    path('reset_password_complete/', views.PasswordResetCompleteView.as_view(template_name="comptes/password_reset_done.html"), name='password_reset_complete'),
]
