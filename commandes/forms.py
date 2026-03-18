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
    
class OrderItemForm(forms.ModelForm):
        class Meta:
            model = OrderItem
            fields = ("product", "quantity", "price")    
            
        def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                if self.instance and self.instance.pk:
                    # garde le prix existant pour les items existants
                    self.fields['price'].initial = self.instance.price
                # ajoute une classe pour JS
                self.fields['product'].widget.attrs.update({'class': 'product-select'})
                
                # rendre le champ price readonly
                self.fields['price'].widget.attrs.update({'readonly': 'readonly'})
        
# Formset pour la création (ajoute un formulaire vide pour un nouvel item)
OrderItemFormSetCreate = inlineformset_factory(
    Order,
    OrderItem,
    form=OrderItemForm,
    fields=("product", "quantity", "price"),
    extra=1,
    can_delete=False
)

# Formset pour l’édition (juste les items existants, pas de formulaire vide)
OrderItemFormSetEdit = inlineformset_factory(
    Order,
    OrderItem,
    form=OrderItemForm,
    fields=("product", "quantity", "price"),
    extra=0,
    can_delete=False
)