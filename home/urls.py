from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('aboutus/', views.AboutUsView.as_view(), name='about-us'),
    path('privacy-policy/', views.PrivacyPolicyView.as_view(), name='privacy-policy'),
    path('terms-of-service/', views.TermsofServiceView.as_view(), name='terms-of-service'),
] 