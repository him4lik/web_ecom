from django.urls import path
from . import views

urlpatterns = [
    path('', views.CheckoutView.as_view(), name='checkout'),
    path('payment/', views.PaymentView.as_view(), name='payment'),
    path('razorpay/callback/', views.RazorpayCallback.as_view(), name="razorpay-callback"),
    path('payment/success/', views.PaymentSuccessView.as_view(), name='payment-success'),
    path('payment/failed/', views.PaymentFailedView.as_view(), name='payment-failed'),
]