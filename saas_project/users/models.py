from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    email=models.EmailField(unique=True)
    is_verified=models.BooleanField(default=False)
    
    #Gestion des roles
    ROLE_CHOICES=(
        ("admin","Admin"),
        ("user","User"),
    )
    role=models.CharField(max_length=10, choices=ROLE_CHOICES,default="user")
    
    #identifiant pour la connexion
    USERNAME_FIELD="email"
    REQUIRED_FIELDS=["username"]
    
    #méthode pour vérifier le role
    def is_admin(self):
        return self.role=="admin"
    
    def is_user(self):
        return self.role=="user"
    
    def __str__(self):
        return self.email