import requests
from django.http import JsonResponse
from web_ecom.settings import API_HOST
from lib.backend_apis import get_as_user, post_as_user, add_to_cart

def AddToCartView(request):
    action = request.GET.get('action', '')
    variant_id = request.GET.get('variant_id', '')
    data = {
        "action":action,
        "variant_id":variant_id
    }
    resp = add_to_cart(data, request.api_headers)
    
    return JsonResponse({
    	"quantity":resp.get('quantity', 0),
        "subtotal":resp.get('subtotal', 0),
        "success": True
    	})

def SendOTP(request):
    username = request.GET.get('username')
    payload = {
        "username":username,
    }
    resp = post_as_user(f"{API_HOST}user/request-otp/", payload)
    
    return JsonResponse(resp)