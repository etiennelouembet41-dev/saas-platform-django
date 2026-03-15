from django.shortcuts import render, redirect, get_object_or_404
from .models import Invoice
from django.views.generic import ListView, DetailView

# Create your views here.
class InvoiceListView(ListView):
    model=Invoice
    
    template_name="factures/invoice_list.html"
    
    context_object_name="invoices"
    

class InvoiceDetailView(DetailView):
    model=Invoice
    
    template_name="factures/invoice_detail.html"
    
    context_object_name="invoice"
    