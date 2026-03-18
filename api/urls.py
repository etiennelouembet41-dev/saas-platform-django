from django.urls import path, include
from rest_framework.routers import DefaultRouter

#ici on fait venir les vues avec le nom des apps 
from clients.views import ClientViewSet 
from produits.views import ProductViewSet
from commandes.views import OrderViewSet

router=DefaultRouter()

router.register(r'clients', ClientViewSet)

#router.register("clients",ClientViewSet)
router.register("produits",ProductViewSet)
router.register("orders",OrderViewSet)

urlpatterns = [
    path("",include(router.urls)),
]
