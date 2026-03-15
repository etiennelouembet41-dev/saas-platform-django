from django.urls import path
from .views import InvoiceListView,InvoiceDetailView

urlpatterns = [
    path("", InvoiceListView.as_view(), name="invoice_list"),
    path("<int:pk>/", InvoiceDetailView.as_view(), name="invoice_detail"),
]
