from rest_framework.decorators import api_view
from rest_framework.response import Response
from commandes.models import Order,OrderItem
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.db.models import Count

@api_view(["GET"])
def order_stats(request):
    stats=(
        Order.objects
                    .annotate(month=TruncMonth("created_at"))
                    .values("month")
                    .annotate(total=Sum("total"))
                    .order_by("month")
    )
    
    data= {
        "labels":[s["month"].strftime("%Y-%m") for s in stats],
        "data":[s["total"] for s in stats],
    }
    
    return Response(data)


#Graphique commandes
@api_view(["GET"])
def orders_count_stats(request):
    
    stats=(
        Order.objects
        .annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(total=Count("id"))
        .order_by("month")
    )
    
    # Formater la date en chaîne YYYY-MM
    data = [
        {"month": s["month"].strftime("%Y-%m"), "total": s["total"]}
        for s in stats
    ]
    
    return Response(data)


@api_view(["GET"])
def top_products(request):
    
    stats=(
        OrderItem.objects
        .values("product__name")
        .annotate(total=Sum("quantity"))
        .order_by("-total")[:5]
    )
    
    data={
        "labels":[s["product__name"] for s in stats],
        "data": [s["total"] for s in stats],
    }
    
    return Response(data)
