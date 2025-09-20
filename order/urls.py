from django.urls import path
from . import views

urlpatterns = [
    path('', views.OrdersView.as_view(), name='user-orders'),
    path('detail/', views.OrderDetailView.as_view(), name='order-detail'),
]