import re

from django.utils.text import slugify
from rest_framework import serializers

from .models import Cliente, Calculo

class ClienteSerializer(serializers.ModelSerializer):
    cpf = serializers.CharField(required=True, allow_blank=False, trim_whitespace=True)

    class Meta:
        model = Cliente
        fields = '__all__'
        extra_kwargs = {
            'cpf': {'validators': []},
        }

    def _validate_cpf(self, cpf):
        cpf = re.sub(r'\D', '', cpf or '')
        if len(cpf) != 11 or not cpf.isdigit():
            return None

        if len(set(cpf)) == 1:
            return None

        def calcular_digito(cpf_parcial, pesos):
            total = sum(int(digito) * peso for digito, peso in zip(cpf_parcial, pesos))
            resto = total % 11
            return '0' if resto < 2 else str(11 - resto)

        primeiro_digito = calcular_digito(cpf[:9], range(10, 1, -1))
        segundo_digito = calcular_digito(cpf[:9] + primeiro_digito, range(11, 1, -1))
        if cpf[-2:] != primeiro_digito + segundo_digito:
            return None
        return cpf

    def validate_cpf(self, value):
        cpf = self._validate_cpf(value)
        if cpf is None:
            raise serializers.ValidationError('CPF inválido.')
        return cpf

    def validate_nome(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('Nome é obrigatório.')
        return value.strip()

    def create(self, validated_data):
        validated_data['cpf'] = re.sub(r'\D', '', validated_data.get('cpf', ''))
        validated_data['nome'] = slugify(validated_data['nome']).upper().replace('-', ' ')
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'cpf' in validated_data:
            validated_data['cpf'] = re.sub(r'\D', '', validated_data['cpf'])
        if 'nome' in validated_data:
            validated_data['nome'] = slugify(validated_data['nome']).upper().replace('-', ' ')
        return super().update(instance, validated_data)

class CalculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calculo
        fields = '__all__'