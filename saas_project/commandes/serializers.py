from rest_framework import serializers
from .models import Order,OrderItem
from django.contrib.auth import get_user_model

User = get_user_model()  # récupère TON modèle personnalisé

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=OrderItem
        
        fields=[
            "id",
            "product",
            "quantity",
            "price",
        ]
        
class OrderSerializer(serializers.ModelSerializer):
    
    items = OrderItemSerializer(many=True)
    
    class Meta:
        model=Order
        
        fields=[
            "id",
            "client",
            "statuts",
            "items",
            "total",
        ]
    
    def create(self, validated_data):
        #user = self.context['request'].user  # ← prend l'utilisateur connecté
        items_data=validated_data.pop("items")

        # Utiliser un utilisateur existant pour test
        user = get_user_model().objects.get(id=1)
        
        order=Order.objects.create(user=user, **validated_data)

        for item_data in items_data :
            OrderItem.objects.create(
                order=order,
                **item_data
            )
        
        order.calculate_total()

        return order
        