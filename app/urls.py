from django.urls import path, include
from app import views


urlpatterns = [
    path('', views.sale_list_view, name='home'),
    path('search/', views.search_view, name='search'),
    path('sales/', views.sale_list_view),
    path('sales/create/', views.sale_create_view, name='sale_create'),
    path('sales/stage-<slug:stage>/', views.sale_list_view, name='sale_stages'),
    path('sales/sale-<int:id>/', views.sale_detail_view, name='sale_detail'),
]