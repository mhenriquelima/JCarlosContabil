from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .viewsets import CalculoViewSet, ClienteViewSet

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet, basename='cliente')
router.register(r'calculos', CalculoViewSet, basename='calculo')

urlpatterns = [
    path('', include(router.urls)),
]
