from lib.base_classes import BaseTemplateView
from lib.backend_apis import (
    get_categories,
    get_featured_products,
)
from home.models import CompanyINFO

class HomePageView(BaseTemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['categories'] = get_categories(self.request.api_headers)
        context['featured'] = get_featured_products({"limit":4}, self.request.api_headers)
        return context

class AboutUsView(BaseTemplateView):
    template_name = "aboutus.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        return context

class PrivacyPolicyView(BaseTemplateView):
    template_name = "privacy_policy.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        return context

class TermsofServiceView(BaseTemplateView):
    template_name = "terms_of_service.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        return context
