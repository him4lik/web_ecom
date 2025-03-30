from lib.base_classes import BaseTemplateView

class OrderView(BaseTemplateView):
    template_name = "user_orders.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # Get default context
        return context

class OrderTrackingView(BaseTemplateView):
    template_name = "order_tracking.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # Get default context
        return context