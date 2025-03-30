import requests
from web_ecom.settings import API_HOST

def get_as_user(url, params={}, headers={}):
	response = requests.get(url, params=params, headers=headers)
	print(response)
	data = response.json()
	return data

def post_as_user(url, data={}, headers={}):
	response = requests.post(url, data=data, headers=headers)
	data = response.json()
	return data

def get_categories(headers):
	url = f"{API_HOST}inventory/categories/"
	params = {}
	resp = get_as_user(url, params)
	return resp

def get_variants(params, headers):
	url = f"{API_HOST}inventory/filter/"
	resp = get_as_user(url, params, headers)
	return resp

def get_featured_products(params, headers):
	url = f"{API_HOST}inventory/featured/"
	resp = get_as_user(url, params, headers)
	return resp

def get_cart_data(headers):
	url = f"{API_HOST}cart/"
	resp = get_as_user(url, headers=headers)
	return resp

def get_user(access_token, refresh_token):
	url = API_HOST+'user/authenticate/'
	data = {
		"refresh_token": refresh_token
	}
	response = requests.post(url, json=data, headers = {'Authorization': f"Bearer {access_token}", 'Content-Type': 'application/json'})
	if response.status_code == 401:
		return {}
	data = response.json()
	
	return data

def add_to_cart(data, headers):
	url = f"{API_HOST}cart/add-to-cart/"
	resp = post_as_user(url, data, headers)
	return resp

def get_variant_details(variant_slug, headers):
	url = f"{API_HOST}inventory/details/"
	params = {"variant_slug": variant_slug}
	resp = get_as_user(url, params, headers=headers)
	return resp
