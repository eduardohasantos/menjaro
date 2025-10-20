from django.urls import path
from . import views

# Define um namespace para a app, se desejar (boa prática)
app_name = 'noticias'

urlpatterns = [
    path('<int:pk>/', views.detalhe_noticia, name='detalhe_noticia'),
]