from django.shortcuts import render,redirect,get_object_or_404
from rest_framework import viewsets
from .models import Order
from .serializers import OrderSerializer
from .forms import OrderForm, OrderItemFormSetCreate,OrderItemFormSetEdit
# Create your views here.

class OrderViewSet(viewsets.ModelViewSet):
    queryset=Order.objects.all()

    serializer_class=OrderSerializer

#pour voir les commande    
def order_list(request):
    
    orders=Order.objects.all()
    
    context={
        "orders":orders
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