from django.db import models
from django.conf import settings
from clients.models import Client
from produits.models import Products
# Create your models here.

class Order(models.Model):
    
    user=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    
    client=models.ForeignKey(
        Client,
        on_delete=models.CASCADE
    )
    
    created_at=models.DateTimeField(auto_now_add=True)

    statuts=models.CharField(
        max_length=20,
        choices=[
            ("pending","Pending"),
            ("paid","Paid"),
            ("cancelled","Cancelled"),
        ],
        default="pending"
    )
    
    total=models.DecimalField(
        max_digits=20, 
        decimal_places=2,
        default=0
    ) 
    
    def __str__(self):
        return f"Order{self.id}"
    
    def calculate_total(self):
        
        total=sum(
            item.get_total()
            for item in self.items.all()
        )
        self.total=total
        self.save()
        
    @property #pour permettre à ce qu'on l'ajoute dans le template
    def total_quantity(self):
        return sum(item.quantity for item in self.items.all()) 
    
class OrderItem(models.Model):
    order=models.ForeignKey(
        Order,
        related_name="items",
        on_delete=models.CASCADE
    )
    
    product=models.ForeignKey(
        Products,
        on_delete=models.CASCADE
    )
    
    quantity=models.IntegerField(default=1)
    
    price=models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    
    def get_total(self):
        return self.quantity * self.price
    
class Invoice(models.Model): #pour la facture
    order=models.OneToOneField(
        Order,
        on_delete=models.CASCADE
    )
    
    created_at=models.DateTimeField(auto_now_add=True)

    total=models.DecimalField(
        max_digits=20,
        decimal_places=2
    )
    
    