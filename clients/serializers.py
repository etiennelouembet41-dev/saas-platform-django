from rest_framework import serializers
from .models import Client
from rest_framework.permissions import IsAdminUser

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model= Client
        
        fields="__all__"