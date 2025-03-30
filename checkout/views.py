from lib.base_classes import BaseTemplateView

class CheckoutView(BaseTemplateView):
    template_name = "checkout.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        return context

class PaymentView(BaseTemplateView):
    template_name = "payment.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context