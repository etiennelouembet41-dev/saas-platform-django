from django.urls import path
from .views import signup_view,CustomLoginView,CustomLogoutView,activate_account,email_sent_view
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("signup/", signup_view, name="signup"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    
    #pour la rénitialisation du mot de passe 
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name="users/password_reset.html"), name="password_reset" ),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"),name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="users/password_reset_confirm.html",
            success_url="/users/password-reset-complete/"), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"),name="password_reset_complete"),
    
    #pour l'activation de l'identifiant utilisateur lors de l'inscription
    path("activate/<uidb64>/<token>/", activate_account, name="activate"),
    path("email-sent/", email_sent_view, name="email_sent" ),
]
