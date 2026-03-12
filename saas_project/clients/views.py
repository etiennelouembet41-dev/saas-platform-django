from django.shortcuts import render,redirect,get_object_or_404
from rest_framework import viewsets
from .serializers import ClientSerializer
from .models import Client
from rest_framework.permissions import IsAuthenticated
from .forms import ClientForm
# Create your views here.

class ClientViewSet(viewsets.ModelViewSet):
    queryset=Client.objects.all()

    serializer_class=ClientSerializer
    
    permission_classes=[IsAuthenticated]


#pour afficher la liste des clients
def clients_list(request):
    
    clients=Client.objects.all()
    
    context={
        "clients":clients
    }

    return render(
        request,
        "clients/clients_list.html",
        context
        
    )
    

#pour créer une liste
def client_create(request):
    
    form=ClientForm(request.POST or None)
    
    if form.is_valid():
        client=form.save(commit=False)
        client.user=request.user #pour reconnaitre directement l'utilisateur conneccté lors de l'ajout d'un client
        form.save()

        return redirect("clients_list")
    
    return render(request, "clients/client_form.html", {"form":form})


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