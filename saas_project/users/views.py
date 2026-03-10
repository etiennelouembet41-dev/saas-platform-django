from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login
from .forms import SignupForm #le formulaire
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from users.models import User #modèle user personnalisé
from django.contrib.auth.decorators import permission_required

# Create your views here.
def signup_view(request):
    
    if request.method=="POST":
        form=SignupForm(request.POST)
        
        if form.is_valid():
            user=form.save()
            ###
            user.is_active=False
            user.save()
            #login(request, user)
            
            current_site=get_current_site(request)
            domain = f"{current_site.domain}"#inclu le port
            
            mail_subject="Active Ton compte"
            
            message=render_to_string("users/email_verification.html",
                           {
                               "user":user,
                               "domain":domain,
                               "uid":urlsafe_base64_encode(force_bytes(user.pk)),
                               "token":default_token_generator.make_token(user)

                           }
                
            )
            
            email=EmailMessage(
                mail_subject,
                message,
                to=[user.email]
            )
            
            email.send()
        
            return render(request,"users/email_sent.html")
    
    else:
        form=SignupForm()
        
    return render(request, "users/signup.html", {"form":form})


def activate_account(request,uidb64, token):
    
        # Décodage de l'UID
    uid = force_str(urlsafe_base64_decode(uidb64))
        # Récupération sécurisée de l'utilisateur
    user = get_object_or_404(User, pk=uid)
        
    if default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        
        #connexion automatique
        login(request, user)

        #redirection vers le dashboard
        return redirect("dashboard")
    
    # Token invalide
    return redirect("login")


def email_sent_view(request):
    return render(request, "users/email_sent.html")

class CustomLoginView(LoginView):
    template_name="users/login.html"
  
    
class CustomLogoutView(LogoutView):
    next_page="login"
