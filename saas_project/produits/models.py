from django.db import models
from django.conf import settings
# Create your models here.

class Products(models.Model):
    
    user=models.ForeignKey( 
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    
    name=models.CharField(max_length=500)

    description=models.TextField()

    price=models.DecimalField(max_digits=10, decimal_places=2)

    stock=models.IntegerField(default=0)

    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name