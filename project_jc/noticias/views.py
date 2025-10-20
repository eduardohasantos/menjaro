from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import Noticia

def detalhe_noticia(request, pk):
    """
    Exibe uma única notícia com base na sua chave primária (pk).
    """

    noticia = get_object_or_404(Noticia, pk=pk)
    

    contexto = {
        'noticia': noticia
    }
    

    return render(request, 'noticias/noticia_detalhe.html', contexto)