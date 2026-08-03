from django.contrib import admin
from .models import Cliente, Calculo


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('cpf', 'nome')
    search_fields = ('cpf', 'nome')


@admin.register(Calculo)
class CalculoAdmin(admin.ModelAdmin):
    list_display = ('inscricao', 'cliente', 'valor', 'status', 'data_de_modificacao')
    list_filter = ('status', 'data_de_modificacao')
    search_fields = ('inscricao', 'cliente__nome', 'cliente__cpf', 'valor')
    raw_id_fields = ('cliente',)
    readonly_fields = ('data_de_modificacao',)