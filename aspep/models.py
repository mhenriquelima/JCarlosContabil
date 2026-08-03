from django.core.validators import RegexValidator
from django.db import models

from .utils import cliente_microfilmagens_upload_to, cliente_extrato_upload_to

# Create your models here.
class Cliente(models.Model):
    cpf = models.CharField(
        max_length=11,
        primary_key=True,
        validators=[RegexValidator(r'^\d{11}$', 'CPF deve conter 11 dígitos numéricos.')],
        verbose_name='CPF',
    )
    nome = models.CharField(max_length=50, verbose_name='Nome')

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return f'{self.nome} ({self.cpf})'

class Calculo(models.Model):

    class Status(models.TextChoices):
        PENDENTE = 'P', 'PENDENTE'
        REFAZER = 'R', 'REFAZER'
        CORRETO = 'C', 'CORRETO'
    
    inscricao = models.CharField(max_length=12, primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name='Cliente')
    valor = models.CharField(max_length=10, verbose_name='Valor')
    status = models.CharField(
            max_length=1,
            choices=Status.choices,
            default=Status.PENDENTE,
            verbose_name='Status',
        )
    microfilmagens = models.FileField(upload_to=cliente_microfilmagens_upload_to, verbose_name='Microfilmagens')
    extrato = models.FileField(upload_to=cliente_extrato_upload_to, verbose_name='Extrato')
    observacoes_adcionais = models.TextField(blank=True, verbose_name='Observações adicionais')
    data_de_modificacao = models.DateTimeField(auto_now=True, verbose_name='Data de modificação')

    class Meta:
        verbose_name = 'Cálculo'
        verbose_name_plural = 'Cálculos'

    def __str__(self):
        return f'{self.inscricao} - {self.cliente.nome} ({self.valor}) - {self.get_status_display()}'