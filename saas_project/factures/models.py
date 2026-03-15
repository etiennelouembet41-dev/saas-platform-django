from django.db import models
from clients.models import Client
from commandes.models import Order
from produits.models import Products
from django.conf import settings
# Create your models here.
 
 
class Invoice(models.Model):
    
    order=models.OneToOneField(
        Order,
        on_delete=models.CASCADE
    ) 
    
    invoice_number=models.CharField(
        max_length=50,
        unique=True
    )
    
    created_at=models.DateTimeField(auto_now_add=True)

    total=models.DecimalField(
        max_digits=20,
        decimal_places=2
    )
    
    is_paid=models.BooleanField(default=False)

    def __str__(self):
        return f"Invoice  {self.invoice_number}"