from django.utils.text import slugify

def _get_cliente_nome_slug(instance):
    cliente = getattr(instance, 'cliente', None)
    if cliente is not None:
        return slugify(cliente.nome)

    if hasattr(instance, 'nome'):
        return slugify(instance.nome)

    return 'cliente'

def cliente_microfilmagens_upload_to(instance, filename):
    nome_slug = _get_cliente_nome_slug(instance)
    return f'documentos/{nome_slug}/microfilmagens/{filename}'

def cliente_extrato_upload_to(instance, filename):
    nome_slug = _get_cliente_nome_slug(instance)
    return f'documentos/{nome_slug}/extrato/{filename}'