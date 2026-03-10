from django.db import models
from django.conf import settings
# Create your models here.

class Client(models.Model):
    user=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE 
    )
    
    name=models.CharField(max_length=300)

    email=models.EmailField()

    phone=models.CharField(max_length=20)

    address=models.TextField()

    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name