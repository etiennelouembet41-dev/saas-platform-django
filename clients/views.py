from django.shortcuts import render,redirect,get_object_or_404
from rest_framework import viewsets
from .serializers import ClientSerializer
from .models import Client
from rest_framework.permissions import IsAdminUser
from .forms import ClientForm
from django.core.paginator import Paginator
from django.db.models import Q
import openpyxl
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from users.decorators import admin_required
# Create your views here.


class ClientViewSet(viewsets.ModelViewSet):
    queryset=Client.objects.all()

    serializer_class=ClientSerializer
    
    permission_classes=[IsAdminUser]


@login_required
#pour afficher la liste des clients
def clients_list(request):
    
    sort=request.GET.get("sort") #en ce qui concerne le tri
    
    search_query=request.GET.get("search") #en ce qui concerne la recherche
    
    clients=Client.objects.all() 
    
    if search_query:
        clients=clients.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone__icontains=search_query) 
            
        )
    
    if sort:
        clients=clients.order_by(sort)
        
    
    paginator=Paginator(clients, 10) # 10 clients par page
    
    page_number=request.GET.get("page") #en ce qui concerne la pagination
    
    page_obj=paginator.get_page(page_number)
    
    context={ "clients":page_obj,
                "search_query":search_query,
                "sort": sort   
            } 
    
    return render( 
                  request, 
                  "clients/clients_list.html", 
                  context )
    
@login_required
#pour créer une liste
def client_create(request):
    
    form=ClientForm(request.POST or None)
    
    if form.is_valid():
        client=form.save(commit=False)
        client.user=request.user #pour reconnaitre directement l'utilisateur conneccté lors de l'ajout d'un client
        form.save()

        return redirect("clients_list")
    
    return render(request, "clients/client_form.html", {"form":form})


@login_required
#pour modifier une liste
def client_edit(request, id):
    
    client=get_object_or_404(Client, id=id)# id =id très important pour reconnaitre l'id du client
    
    form=ClientForm(request.POST or None, instance=client)

    if form.is_valid():
        form.save()

        return redirect("clients_list")

    return render(
        request,
        "clients/client_form.html",
        {"form":form}
    )

@login_required
@admin_required
#pour supprimer un client
def client_delete(request, id):
    
    client=get_object_or_404(Client, id=id)

    if request.method=="POST":
        
        client.delete()
        
        return redirect("clients_list")
    
    return render( request, 
                  "clients/client_delete.html",
                  {"client":client}
                )
    
@login_required    
#pour télécharger un fichier excel
def export_clients_excel(request):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Clients"

    # En-têtes
    sheet.append(["Name", "Email", "Phone"])

    # Données clients
    clients = Client.objects.all()
    for client in clients:
        sheet.append([client.name, client.email, client.phone])

    # Réponse Excel
    response = HttpResponse(content_type="application/ms-excel")
    response["Content-Disposition"] = 'attachment; filename="clients.xlsx"'
    workbook.save(response)
    return response