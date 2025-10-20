from django.db import models

# Create your models here.

from django.db import models

class Noticia(models.Model):
    """
    Modelo para armazenar o conteúdo de uma notícia.
    """
    titulo = models.CharField(max_length=200, help_text="O título da notícia")
    corpo = models.TextField(help_text="O conteúdo principal da notícia")
    data_publicacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Publicação")

    class Meta:
        verbose_name = "Notícia"
        verbose_name_plural = "Notícias"

    def __str__(self):
        return self.titulo
    
    