import hmac, hashlib
from django.shortcuts import redirect, render
from django.contrib import messages
from django.utils.decorators import method_decorator

from lib.base_classes import BaseTemplateView
from lib.backend_apis import (
    get_cart_data,
    get_profile_data,
    update_profile,
    create_order,
    make_payment,
    get_order_details,
    get_orders_data,
)
from user.decorators import login_required
from user.forms import AddressForm
from web_ecom.settings import RZP_KEY_ID, RZP_SECRET_KEY
from home.models import CompanyINFO


@method_decorator(login_required(), name="dispatch")
class CheckoutView(BaseTemplateView):
    """
    Handles checkout page rendering and adding/updating addresses.
    """
    template_name = "checkout.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cart"] = get_cart_data(self.request.api_headers)

        profile_data = get_profile_data(self.request.api_headers)
        context["addresses"] = profile_data.get("addresses", [])

        context["address_form"] = AddressForm()
        return context

    def post(self, request):
        address_form = AddressForm(request.POST)
        if address_form.is_valid():
            address_data = {
                "address": {
                    "type": address_form.cleaned_data.get("type", ""),
                    "name": address_form.cleaned_data.get("name", ""),
                    "phone": address_form.cleaned_data.get("phone", ""),
                    "line1": address_form.cleaned_data.get("line1", ""),
                    "line2": address_form.cleaned_data.get("line2", ""),
                    "city": address_form.cleaned_data.get("city", ""),
                    "state": address_form.cleaned_data.get("state", ""),
                    "pin": address_form.cleaned_data.get("pin", ""),
                    "landmark": address_form.cleaned_data.get("landmark", ""),
                }
            }
            update_profile(address_data, self.request.api_headers)
            return redirect(request.path)

        context = self.get_context_data()
        context["address_form"] = address_form
        return render(request, self.template_name, context)

@method_decorator(login_required(), name="dispatch")
class PaymentView(BaseTemplateView):
    """
    Handles order creation, payment initiation via Razorpay,
    and displays the user orders page.
    """
    template_name = "user_orders.html"

    def post(self, request):
        phone = request.POST.get("phone")
        order_id = request.POST.get("order_id")

        if not order_id and not phone:
            messages.error(request, "Please select a shipping address before proceeding.")
            return redirect("checkout")

        if not order_id:
            resp = create_order({"phone": phone}, self.request.api_headers)
            order_id = resp.get("order_id")

        order_details = get_order_details({"order_id": order_id}, request.api_headers)

        context = {
            "order_details": order_details.get("order", {}),
            "order_id": order_id,
            "KEY_ID": RZP_KEY_ID,
            "company": CompanyINFO.objects.last(),
            "api_user": request.api_user,
            "open_razorpay": True,
        }

        payload = {
            "offset": self.request.GET.get("offset", 0),
            "limit": self.request.GET.get("limit", 10),
        }
        orders = get_orders_data(payload, self.request.api_headers)

        context["orders"] = orders.get("orders", [])
        pagination = orders.get("pagination", {})
        context["limit"] = pagination.get("limit", 10)
        context["offset"] = pagination.get("offset", 0)
        context["total"] = pagination.get("total", 0)
        context["has_more"] = pagination.get("has_more", False)
        context["prev_offset"] = max(context["offset"] - context["limit"], 0)

        return render(request, self.template_name, context)


@method_decorator(login_required(), name="dispatch")
class RazorpayCallback(BaseTemplateView):
    """
    Handles Razorpay payment callback:
    - Validates payment signature
    - Calls backend API to finalize payment
    - Redirects to success/failure page
    """
    def post(self, request):
        razorpay_payment_id = request.POST.get("razorpay_payment_id")
        razorpay_order_id = request.POST.get("razorpay_order_id")
        razorpay_signature = request.POST.get("razorpay_signature")

        generated_signature = hmac.new(
            bytes(RZP_SECRET_KEY, "utf-8"),
            msg=f"{razorpay_order_id}|{razorpay_payment_id}".encode(),
            digestmod=hashlib.sha256,
        ).hexdigest()

        if generated_signature == razorpay_signature:
            payload = {
                "razorpay_payment_id": razorpay_payment_id,
                "razorpay_order_id": razorpay_order_id,
                "razorpay_signature": razorpay_signature,
            }
            resp = make_payment(payload, request.api_headers)
            if resp.get("success", False):
                return redirect("payment-success")

        return redirect("payment-failed")

@method_decorator(login_required(), name="dispatch")
class PaymentSuccessView(BaseTemplateView):
    template_name = "payment_success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"status": "success", "notification_type": "payment"})
        return context


@method_decorator(login_required(), name="dispatch")
class PaymentFailedView(BaseTemplateView):
    template_name = "payment_failed.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"status": "failed", "notification_type": "payment"})
        return context
