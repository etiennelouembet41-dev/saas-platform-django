from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ClientSerializer
from .models import Client
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class ClientViewSet(viewsets.ModelViewSet):
    queryset=Client.objects.all()

    serializer_class=ClientSerializer
    
    permission_classes=[IsAuthenticated]
