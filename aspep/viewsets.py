from rest_framework import viewsets

from aspep.filters import CalculoFilter, ClienteFilter

from .models import Cliente, Calculo
from .serializers import ClienteSerializer, CalculoSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    filterset_class = ClienteFilter

class CalculoViewSet(viewsets.ModelViewSet):
    queryset = Calculo.objects.all()
    serializer_class = CalculoSerializer
    filterset_class = CalculoFilter