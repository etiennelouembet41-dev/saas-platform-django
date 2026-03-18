from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from .serializers import ProductSerializer
from .models import Products
from .forms import ProductsForm
from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.decorators import login_required
from users.decorators import admin_required
# Create your views here.

class ProductViewSet(viewsets.ModelViewSet):
    queryset=Products.objects.all()

    serializer_class=ProductSerializer
    
    permission_classes=[IsAdminUser]
    

login_required
#pour voir la liste des produits
def products_list(request):
    
    sort=request.GET.get("sort")
    
    search_query=request.GET.get("search")
    
    products=Products.objects.all()
    
    if search_query:
        products=products.filter(
            Q(name__icontains=search_query)|
            Q(description__icontains=search_query)
           
        )
    
    if sort:
        products=products.order_by(sort)
    
    paginator=Paginator(products, 10)

    page_number=request.GET.get("page")
    
    page_obj=paginator.get_page(page_number)

    context={
        "products":page_obj,
        "page_obj": page_obj,               # pour la pagination
        "search_query": search_query        # pour garder la recherche
    }
     
    return render(
        request,
        "produits/products_list.html",
        context
    )
   
login_required    
#pour la création de produits
def products_create(request):
    
    form=ProductsForm(request.POST or None, request.FILES or None) # <- Ajouter request.FILES pour l'image
    
    if form.is_valid():
        products=form.save(commit=False)
        products.user=request.user
        products.save()  # <- ici, sauvegarder l'instance avec save()
        

        return redirect("products_list")
    
    return render(request, "produits/products_form.html", {"form":form})

login_required
#pour modifier un produit
def products_edit(request, id):
    
    products=get_object_or_404(Products, id=id)
    
    form=ProductsForm(request.POST or None, request.FILES or None, instance=products)

    if form.is_valid():
        form.save()

        return redirect("products_list")
    
    return render(request, 
                  "produits/products_form.html",
                  {"form":form}
                )

login_required
@admin_required
#pour supprimer le produit
def products_delete(request, id):
    
    products=get_object_or_404(Products, id=id)

    if request.method=="POST":
        
        products.delete()
        
        return redirect("products_list")
    
    return render(request, 
                  "produits/products_delete.html",
                  {"products":products}
                )
    
    

    