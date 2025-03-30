from django.urls import path
from . import views

urlpatterns = [
    path('', views.OrderView.as_view(), name='user-orders'),
    path('tracking/', views.OrderTrackingView.as_view(), name='tracking'),
]