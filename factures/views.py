from django.shortcuts import render, redirect, get_object_or_404
from .models import Invoice
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from users.decorators import admin_required
from django.utils.decorators import method_decorator

# Create your views here.
@method_decorator(login_required, name='dispatch')
class InvoiceListView(ListView):
    model=Invoice
    
    template_name="factures/invoice_list.html" 
    
    #context_object_name="invoices"
    
    paginate_by = 10
    
    def get_queryset(self):
        qs = super().get_queryset()
        search_query = self.request.GET.get("search", "")
        sort = self.request.GET.get("sort", "")

        if search_query:
            qs = qs.filter(
                Q(order__id__icontains=search_query) |          # ID de la commande
                Q(order__client__name__icontains=search_query) | # Nom du client
                Q(total__icontains=search_query) 
            )
        
        # Tri
        if sort:
            qs = qs.order_by(sort)

        return qs
    
@method_decorator(login_required, name='dispatch')
class InvoiceDetailView(DetailView):
    model=Invoice
    
    template_name="factures/invoice_detail.html"
    
    context_object_name="invoice"
    