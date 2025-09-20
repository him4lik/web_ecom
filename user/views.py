from lib.base_classes import BaseTemplateView
from .forms import LoginForm, ProfileForm, AddressForm
from django.shortcuts import redirect, render
from lib.backend_apis import post_as_user, get_profile_data, update_profile, get_orders_data
from web_ecom.settings import API_HOST
from django.middleware.csrf import get_token
from django.urls import reverse
from django.views import View
import requests
from .decorators import login_required
from django.utils.decorators import method_decorator


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

@method_decorator(login_required(), name='dispatch')
class ProfileView(BaseTemplateView):
    template_name = "user_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # Get default context
        profile_data = get_profile_data(self.request.api_headers)
        payload = {
            "limit":5
        }
        orders = get_orders_data(payload, self.request.api_headers)
        context['orders'] = orders.get('orders', []) 
        context['profile_form'] = ProfileForm(profile_data)
        context['address_form'] = AddressForm()
        context['addresses'] = profile_data.get('addresses', [])
        for i in context['addresses']:
            form = AddressForm({
                "type":i.get('address_type', ''),
                "name":i.get('poc_name', ''),
                "phone":i.get('phone', ''),
                "line1":i.get('line_1', ''),
                "line2":i.get('line_2', ''),
                "city":i.get('city', ''),
                "state":i.get('state', ''),
                "pin":i.get('pin', ''),
                "landmark":i.get('landmark', ''),
                })
            i['form'] = form
        return context

    def post(self, request):
        profile_form = ProfileForm(request.POST)
        address_form = AddressForm(request.POST)
        payload = {
            "limit":5
        }
        orders = get_orders_data(payload, self.request.api_headers)
        context = {"profile_form": profile_form, "address_form": address_form}
        context['orders'] = orders.get('orders', [])
        action = request.POST.get('action', '')
        if profile_form.is_valid():
            resp = update_profile(profile_form.data, self.request.api_headers)
            return redirect(request.path)
        if address_form.is_valid():
            address_data = {"address":{
                "type":address_form.data.get('type', ''),
                "name":address_form.data.get('name', ''),
                "phone":address_form.data.get('phone', ''),
                "line1":address_form.data.get('line1', ''), 
                "line2":address_form.data.get('line2', ''),
                "city":address_form.data.get('city', ''),
                "state":address_form.data.get('state', ''),
                "pin":address_form.data.get('pin', ''),
                "landmark":address_form.data.get('landmark', ''),
                    }
                }
            resp = update_profile(address_data, self.request.api_headers)
            return redirect(request.path)
        if action == 'delete':
            resp = update_profile({'phone':request.POST.get('phone', ''), "action":action}, self.request.api_headers)
            return redirect(request.path)
        return render(request, self.template_name, context)


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











