
from django.db import models
from django.contrib.auth import get_user_model

class Categoria(models.Model):
	nome = models.CharField(max_length=100, unique=True)

	def __str__(self):
		return self.nome

class Noticia(models.Model):
	titulo = models.CharField(max_length=255)
	conteudo = models.TextField()
	data_publicacao = models.DateTimeField(auto_now_add=True)
	categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True, related_name='noticias')
	visualizacoes = models.PositiveIntegerField(default=0)  # Para "mais lidas"

	def __str__(self):
		return self.titulo

class NewsletterSubscription(models.Model):
	email = models.EmailField(unique=True)
	data_cadastro = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.email

class Comentario(models.Model):
	noticia = models.ForeignKey(Noticia, on_delete=models.CASCADE, related_name='comentarios')
	usuario = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
	texto = models.TextField()
	data_comentario = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Comentário de {self.usuario} em {self.noticia}"

# Create your models here.