from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ProductSerializer
from .models import Products
# Create your views here.

class ProductViewSet(viewsets.ModelViewSet):
    queryset=Products.objects.all()

    serializer_class=ProductSerializer