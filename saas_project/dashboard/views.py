from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from clients.models import Client
from produits.models import Products
from commandes.models import Order
# Create your views here.

@login_required
def dashboard_view(request):
    
    clients_count=Client.objects.count()

    products_count=Products.objects.count()

    orders_count=Order.objects.count()

    total_revenue=sum(
        order.total for order in Order.objects.all()
    )
    
    context={
        "clients_count":clients_count,
        "products_count":products_count,
        "orders_count":orders_count,
        "total_revenue" : total_revenue,
    }
    
    return render(request,
                  "dashboard/dashboard.html", 
                  context
                  )