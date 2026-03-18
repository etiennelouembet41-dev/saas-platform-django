from django.shortcuts import render,redirect,get_object_or_404
from rest_framework import viewsets
from .models import Order
from .serializers import OrderSerializer
from .forms import OrderForm, OrderItemFormSetCreate,OrderItemFormSetEdit
from django.core.paginator import Paginator
from django.db.models import Q
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from .emails import send_invoice_email
from rest_framework.permissions import IsAdminUser

from django.contrib.auth.decorators import login_required
from users.decorators import admin_required
# Create your views here.


class OrderViewSet(viewsets.ModelViewSet):
    queryset=Order.objects.all()

    serializer_class=OrderSerializer
    permission_classes=[IsAdminUser]

@login_required
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
    
@login_required
#pour créer des commandes
def order_create(request):
    
    if request.method=="POST":
        form=OrderForm(request.POST)
        formset=OrderItemFormSetCreate(request.POST, prefix="items")
        if form.is_valid() and formset.is_valid():
            order=form.save(commit=False)
            order.user=request.user
            order.save()
            
            formset.instance=order
            formset.save()
            
            order.calculate_total()
            
            if order.statuts == "paid":
                send_invoice_email(order) #pour envoyer le mail au cas ou le statuts est paid 
        
            return redirect("order_list")
    
    else:
        form=OrderForm()
        formset=OrderItemFormSetCreate()
    
    return render(
        request,
        "commandes/order_form.html",
        {"form":form, "formset":formset}
    )
    
@login_required    
#pour la modification d'une commande    
def order_edit(request, id):
    
    order=get_object_or_404(Order, id=id)
    
    if request.method=="POST":
        form=OrderForm(request.POST, instance=order)
        formset = OrderItemFormSetEdit(request.POST, instance=order,prefix="items")
    
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            order.calculate_total()
            
            if form.has_changed() and "statuts" in form.changed_data:
                if form.cleaned_data["statuts"] == "paid":
                    send_invoice_email(order)
             
            return redirect("order_list")
    else:
        form = OrderForm(instance=order)
        formset = OrderItemFormSetEdit(instance=order)  # charge uniquement les items de cette commande

    return render(
        request,
        "commandes/order_form.html",
        {"form":form,"formset": formset}
    )
    

@login_required
@admin_required
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
    
@login_required
#la vue concernant le pdf
def generate_invoice_pdf(request, order_id):
    
    order=Order.objects.get(id=order_id)

    response=HttpResponse(content_type="application/pdf")

    response["Content-Disposition"]=(
        f'attachment; filename="invoice_{order.id}.pdf" '
    )
    
    p=canvas.Canvas(response)

    p.drawString(100, 800, f"Invoice #{order.id}")
    
    p.drawString(100, 750, f"Client : {order.client.name}")

    y=700
    
    for item in order.items.all():
        p.drawString(
            100,
            y,
            f"{item.product.name}x{item.quantity}"
        )
        
        y-=20
        
    p.drawString(100, y - 20, f"Total : {order.total}")    

    p.showPage()

    p.save()
    
    return response