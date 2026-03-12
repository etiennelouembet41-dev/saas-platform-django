from django import forms
from django.forms import inlineformset_factory
from .models import Order,OrderItem

class OrderForm(forms.ModelForm):
    
    class Meta:
        model=Order
        
        fields=[
            "client",
            "statuts",
        ]
        
# Formset pour la création (ajoute un formulaire vide pour un nouvel item)
OrderItemFormSetCreate = inlineformset_factory(
    Order,
    OrderItem,
    fields=("product", "quantity", "price"),
    extra=1,
    can_delete=False
)

# Formset pour l’édition (juste les items existants, pas de formulaire vide)
OrderItemFormSetEdit = inlineformset_factory(
    Order,
    OrderItem,
    fields=("product", "quantity", "price"),
    extra=0,
    can_delete=False
)