from lib.base_classes import BaseTemplateView
from lib.backend_apis import get_cart_data

class CartView(BaseTemplateView):
    template_name = "cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = get_cart_data(self.request.api_headers) 
        return context