from lib.base_classes import BaseTemplateView
from .forms import LoginForm
from django.shortcuts import redirect, render
from lib.backend_apis import post_as_user
from web_ecom.settings import API_HOST
from django.middleware.csrf import get_token
from django.urls import reverse
from django.views import View
import requests

class LoginView(BaseTemplateView):
    template_name = "login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  
        context["form"] = LoginForm()
        return context

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            phone = form.cleaned_data["phone"]
            otp = form.cleaned_data["otp"]

            payload = {
                "username": phone,
                "otp": str(otp)
            }
            tokens = post_as_user(f"{API_HOST}user/verify-otp/", payload)
            print(tokens)
            if not tokens.get("access", None):
                return render(request, self.template_name, {
                    "form": form,
                    "error": "Invalid or expired OTP"
                })

            response = redirect("/")  

            response.set_cookie(
                "access_token",
                tokens["access"],
                httponly=True,    
                # secure=True,    
                samesite="Lax",   
                max_age=3600      
            )

            response.set_cookie(
                "refresh_token",
                tokens["refresh"],
                httponly=True,
                # secure=True,
                samesite="Lax",
                max_age=7 * 24 * 3600  
            )

            
            response.set_cookie(
                "csrftoken",
                get_token(request),
                httponly=False,  
                secure=True,
                samesite="Lax",
                max_age=3600
            )

            return response

        return render(request, self.template_name, {"form": form})

class ProfileView(BaseTemplateView):
    template_name = "user_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # Get default context
        return context

class LogoutView(View):
    redirect_url = 'home'

    def post(self, request):
        access_token = request.COOKIES.get('access_token', '')
        refresh_token = request.COOKIES.get('refresh_token', '')

        # if refresh_token:
        #     self.invalidate_refresh_token(refresh_token)  TODO

        response = redirect(reverse(self.redirect_url))
        response.delete_cookie("access_token", path="/") # httponly=True, secure=True
        response.delete_cookie("refresh_token", path="/") # httponly=True, secure=True

        return response











