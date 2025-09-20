from lib.backend_apis import get_user

class AssignUser(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.api_user, request.token, request.api_headers, flag = self.authenticate_user(request)
        response = self.get_response(request)

        if request.api_user and request.token and flag:
            response.set_cookie(
                key="access_token",
                value=request.token,
                httponly=True,  
                # secure=True,  
                samesite="Lax",  
            )

        return response

    def authenticate_user(self, request):
        access_token = request.COOKIES.get('access_token')
        refresh_token = request.COOKIES.get('refresh_token')
        if not access_token:
            return None, '', {}, False

        data = get_user(access_token, refresh_token)
        user = data.get("user", None)

        if not user or not user.get('is_authenticated'):
            return None, '', {}, False

        access_token = data.get('access_token', access_token)
        flag = True if data.get('access_token', None) else False


        return user, access_token, {'Authorization': f"Bearer {access_token}"} , flag