from lib.base_classes import BaseTemplateView
from user.decorators import login_required
from django.utils.decorators import method_decorator
from lib.backend_apis import get_orders_data

@method_decorator(login_required(), name='dispatch')
class OrdersView(BaseTemplateView):
    template_name = "user_orders.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  
        payload = {
            "offset":self.request.GET.get('offset', 0),
            "limit":self.request.GET.get('limit', 10),
        }
        orders = get_orders_data(payload, self.request.api_headers)
        context['orders'] = orders.get('orders', [])
        pagination = orders.get('pagination', {})
        context['limit'] = pagination.get('limit', 10)
        context['offset'] =  pagination.get('offset', 0)
        context['total'] = pagination.get('total', 10)
        context['has_more'] = pagination.get('has_more', False)
        context['prev_offset'] =  max(context['offset'] - context['limit'], 0)
        return context

@method_decorator(login_required(), name='dispatch')
class OrderDetailView(BaseTemplateView):
    template_name = "order_tracking.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        return context