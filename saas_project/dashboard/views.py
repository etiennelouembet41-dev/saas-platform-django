from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def dashboard_view(request):
    context={
        "total_clients":0,
        "total_commandes":0,
        "total_produits":0
    }
    return render(request, "dashboard/dashboard.html", context)