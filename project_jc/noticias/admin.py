from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Noticia

@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    """
    Configuração da interface de admin para o modelo Noticia.
    """
    list_display = ('titulo', 'data_publicacao')
    search_fields = ('titulo', 'corpo')
    list_filter = ('data_publicacao',)
