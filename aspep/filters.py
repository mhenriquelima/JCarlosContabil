import django_filters

from .models import Calculo, Cliente

class ClienteFilter(django_filters.FilterSet):
    class Meta:
        model = Cliente
        fields = {
            'cpf': ['exact', 'icontains'],
            'nome': ['iexact', 'icontains'],
        }

class CalculoFilter(django_filters.FilterSet):
    class Meta:
        model = Calculo
        fields = {
            'inscricao': ['exact', 'icontains'],
            'cliente__cpf': ['exact', 'icontains'],
            'valor': ['exact', 'lt', 'gt', 'range'],
            'data_de_modificacao': ['exact', 'lt', 'gt', 'range'],
            'status': ['exact'],
        }