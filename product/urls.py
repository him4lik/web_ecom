from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductFilterView.as_view(), name='filter'),
    path('<slug:variant_slug>', views.ProductDetailView.as_view(), name='detail'),
]