from django.urls import path

from .views import CookieTokenObtainPairView, CookieTokenRefreshView

urlpatterns = [
    path('token/', CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
    path('auth/login/', CookieTokenObtainPairView.as_view(), name='auth_login'),
    path('auth/refresh/', CookieTokenRefreshView.as_view(), name='auth_refresh'),
]