from django.test import TestCase

from aspep import utils
from aspep.models import Calculo, Cliente
from aspep.serializers import ClienteSerializer

class CalculoModelTests(TestCase):
    def test_calculo_has_cliente_fk_and_uses_cliente_for_upload_path(self):
        cliente = Cliente(cpf='12345678901', nome='Maria Silva')
        calculo = Calculo(inscricao='202400000001', cliente=cliente, valor='100.00')

        self.assertEqual(calculo.cliente, cliente)
        self.assertEqual(
            utils.cliente_microfilmagens_upload_to(calculo, 'arquivo.pdf'),
            'documentos/maria-silva/microfilmagens/arquivo.pdf',
        )
        self.assertEqual(
            utils.cliente_extrato_upload_to(calculo, 'arquivo.pdf'),
            'documentos/maria-silva/extrato/arquivo.pdf',
        )

class ClienteSerializerTests(TestCase):
    def test_serializer_normalizes_cpf_and_name_on_save(self):
        serializer = ClienteSerializer(
            data={'cpf': '529.982.247-25', 'nome': 'José da Silva'}
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)

        cliente = serializer.save()

        self.assertEqual(cliente.cpf, '52998224725')
        self.assertEqual(cliente.nome, 'JOSE DA SILVA')

    def test_serializer_rejects_invalid_cpf(self):
        serializer = ClienteSerializer(data={'cpf': '123.456.789-00', 'nome': 'Maria'})

        self.assertFalse(serializer.is_valid())
        self.assertIn('cpf', serializer.errors)
