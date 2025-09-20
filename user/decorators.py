from django.shortcuts import redirect
from functools import wraps
from django.urls import reverse

def login_required(redirect_to='login'):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.api_user or not request.api_user.get('is_authenticated', False):
                login_url = reverse(redirect_to)
                path = request.get_full_path()
                return redirect(f'{login_url}?next={path}')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator