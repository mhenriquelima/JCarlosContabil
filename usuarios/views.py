from django.conf import settings

from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


def _cookie_settings(token_lifetime):
    return {
        'httponly': True,
        'secure': False,
        'samesite': 'Lax',
        'path': '/',
        'max_age': int(token_lifetime.total_seconds()),
    }


class CookieTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access_lifetime = getattr(settings, 'SIMPLE_JWT', {}).get(
                'ACCESS_TOKEN_LIFETIME',
                api_settings.ACCESS_TOKEN_LIFETIME,
            )
            refresh_lifetime = getattr(settings, 'SIMPLE_JWT', {}).get(
                'REFRESH_TOKEN_LIFETIME',
                api_settings.REFRESH_TOKEN_LIFETIME,
            )

            response.set_cookie(
                'access',
                response.data.get('access'),
                **_cookie_settings(access_lifetime),
            )
            response.set_cookie(
                'refresh',
                response.data.get('refresh'),
                **_cookie_settings(refresh_lifetime),
            )
            response.data = {
                "message": "Login bem-sucedido"
            }

        return response


class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh')
        if refresh_token and 'refresh' not in request.data:
            request.data['refresh'] = refresh_token

        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access_lifetime = getattr(settings, 'SIMPLE_JWT', {}).get(
                'ACCESS_TOKEN_LIFETIME',
                api_settings.ACCESS_TOKEN_LIFETIME,
            )
            response.set_cookie(
                'access',
                response.data.get('access'),
                **_cookie_settings(access_lifetime),
            )
            response.data = {
                "message": "Token de acesso atualizado com sucesso"
            }

        return response
