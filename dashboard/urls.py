from django.urls import path
from .views import dashboard_view
from .api_views import order_stats,orders_count_stats,top_products

urlpatterns = [
    path('',dashboard_view,name="dashboard"),
    path('stats/orders/', order_stats),
    path('stats/orders-count/', orders_count_stats),
    path('stats/top-products/', top_products),
]
