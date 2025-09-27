from lib.base_classes import BaseTemplateView
from lib.backend_apis import get_cart_data
from user.decorators import login_required
from django.utils.decorators import method_decorator

@method_decorator(login_required(), name='dispatch')
class CartView(BaseTemplateView):
    template_name = "cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if resp.get("success"):
            context["cart"] = resp.get("data", {})
            context["cart_error"] = None
        else:
            context["cart"] = {}
            context["cart_error"] = (
                resp.get("error")
                or f"Unable to fetch cart (status: {resp.get('status')})"
            )

        return context