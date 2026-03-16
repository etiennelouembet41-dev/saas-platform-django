from django.shortcuts import render,redirect,get_object_or_404
from rest_framework import viewsets
from .models import Order
from .serializers import OrderSerializer
from .forms import OrderForm, OrderItemFormSetCreate,OrderItemFormSetEdit
from django.core.paginator import Paginator
from django.db.models import Q
# Create your views here.

class OrderViewSet(viewsets.ModelViewSet):
    queryset=Order.objects.all()

    serializer_class=OrderSerializer

#pour voir les commande     
def order_list(request):
    
    sort=request.GET.get("sort")
    
    search_query=request.GET.get("search")
    
    orders=Order.objects.all()
    
    if search_query:
        orders=orders.filter(
            Q(client__name__icontains=search_query)| #client__name__icontains en fonction du model qui s'appel
            Q(items__product__name__icontains=search_query)|
            Q(statuts__icontains=search_query) 
            
        ).distinct()
    
    if sort:
        orders=orders.order_by(sort)
    
    
    
    paginator=Paginator(orders, 10)
    
    page_number=request.GET.get("page")
    
    page_obj=paginator.get_page(page_number)
    
    context={
        "orders":page_obj,
        "search_query":search_query,
        "sort": sort   
    }

    return render(
        request,
        "commandes/order_list.html",
        context
    )
    

#pour créer des commandes
def order_create(request):
    
    if request.method=="POST":
        form=OrderForm(request.POST)
        formset=OrderItemFormSetCreate(request.POST)
        if form.is_valid() and formset.is_valid():
            order=form.save(commit=False)
            order.user=request.user
            order.save()
            
            formset.instance=order
            formset.save()
            
            order.calculate_total()
        
            return redirect("order_list")
    
    else:
        form=OrderForm()
        formset=OrderItemFormSetCreate()
    
    return render(
        request,
        "commandes/order_form.html",
        {"form":form, "formset":formset}
    )
    
    
#pour la modification d'une commande    
def order_edit(request, id):
    
    order=get_object_or_404(Order, id=id)
    
    if request.method=="POST":
        form=OrderForm(request.POST, instance=order)
        formset = OrderItemFormSetEdit(request.POST, instance=order)
    
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            order.calculate_total()
            return redirect("order_list")
    else:
        form = OrderForm(instance=order)
        formset = OrderItemFormSetEdit(instance=order)  # charge uniquement les items de cette commande

    return render(
        request,
        "commandes/order_form.html",
        {"form":form,"formset": formset}
    )
    


#pour supprimer un commande
def order_delete(request, id):
    order=get_object_or_404(Order, id=id)
    
    if request.method=="POST":
        order.delete()
        
        return redirect("order_list")
    
    return render(
        request,
        "commandes/order_delete.html",
        {"order":order}
    )