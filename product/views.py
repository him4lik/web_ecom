from lib.base_classes import BaseTemplateView
from lib.backend_apis import get_variants, get_categories, get_variant_details

class ProductFilterView(BaseTemplateView):
    template_name = "product_filter.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


        params = {
            "category" : self.request.GET.get("category", None),
            "product_id" : self.request.GET.get("product_id", None),
            "search_str" : self.request.GET.get("search_str", "").strip(),
            "featured_prod_id" : self.request.GET.get("featured_prod_id", None), 
            "skip" : int(self.request.GET.get("skip", 0)) if self.request.GET.get("skip", 0) else 0,
            "limit" : int(self.request.GET.get("limit", 8)) if self.request.GET.get("limit", 8) else 8,
        }  
        variants = get_variants(params, self.request.api_headers)
        context['variants'] = variants
        context['categories'] = get_categories(self.request.api_headers)
        pagination = variants.get('pagination', {})
        context['limit'] = pagination.get('limit', 10)
        context['skip'] =  pagination.get('skip', 0)
        context['total'] = pagination.get('total', 10)
        context['has_more'] = pagination.get('has_more', False)
        context['prev_offset'] =  max(context['skip'] - context['limit'], 0)
        context['category'] = variants.get('category', '')
        context['product_id'] = variants.get('product_id', None)
        context['featured_prod_id'] = variants.get('featured_prod_id', None)
        context['search_str'] = variants.get('search_str', '')
        return context

class ProductDetailView(BaseTemplateView):
    template_name = "product_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        variant_slug = self.kwargs.get("variant_slug")
        if variant_slug:
            context['variant'] = get_variant_details(variant_slug, self.request.api_headers)
        return context
