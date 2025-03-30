from django.urls import path
from . import views

urlpatterns = [
    path('add-to-cart/', views.AddToCartView, name='add-to-cart'),
    path('send-otp/', views.SendOTP, name='send-otp')
] 