from django.contrib import admin

# Register your models here.

# app_name/admin.py

from django.contrib import admin
from .models import Categoria, Noticia, NewsletterSubscription, Comentario

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    
    search_fields = ('nome',)

class ComentarioNaNoticia(admin.TabularInline):
    model = Comentario
    readonly_fields = ('usuario', 'texto', 'data_comentario') # Campos nao editaveis
    extra = 0
  
    can_delete = False

@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):

    list_display = ('titulo', 'categoria', 'data_publicacao', 'visualizacoes')
    list_filter = ('categoria', 'data_publicacao')
    search_fields = ('titulo', 'conteudo')
    date_hierarchy = 'data_publicacao'
    readonly_fields = ('data_publicacao', 'visualizacoes')
    inlines = [ComentarioNaNoticia] 
    

    fieldsets = (
        (None, {
            'fields': ('titulo', 'conteudo', 'categoria')
        }),
        ('Dados do Sistema', { 
            'fields': ('data_publicacao', 'visualizacoes'),
            'classes': ('collapse',)
        }),
    )

@admin.register(NewsletterSubscription)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'data_cadastro')
    search_fields = ('email',)
    readonly_fields = ('data_cadastro',)

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):

    list_display = ('noticia', 'usuario', 'data_comentario', 'resumo_do_texto')
    list_filter = ('data_comentario',)
    search_fields = ('texto', 'usuario__username', 'noticia__titulo')
    readonly_fields = ('data_comentario', 'noticia', 'usuario', 'texto')

    def resumo_do_texto(self, obj):
        if len(obj.texto) > 60:
            return f'{obj.texto[:60]}...'
        return obj.texto

    resumo_do_texto.short_description = 'Trecho do Comentário'

