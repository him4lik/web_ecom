from lib.base_classes import BaseTemplateView
from lib.backend_apis import (
    get_categories,
    get_featured_products,
)

class HomePageView(BaseTemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        print(self.request.user)
        context = super().get_context_data(**kwargs) 
        context['categories'] = get_categories(self.request.api_headers)
        context['featured'] = get_featured_products({"limit":4}, self.request.api_headers)
        return context

class AboutUsView(BaseTemplateView):
    template_name = "aboutus.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # Get default context
        return context
