from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Noticia, Categoria
from .forms import SubscriptionForm
from django.views.generic import ListView
from django.views.decorators.http import require_POST
from django.db.models import Q


class HomeView(View):
    def get(self, request):
        noticias = Noticia.objects.order_by('-data_publicacao')
        favoritos_ids = request.session.get('favoritos', [])
        context = {
            "form": SubscriptionForm(),
            "noticias": noticias,
            "favoritos_ids": favoritos_ids
        }
        return render(request, "app1/home.html", context)

class SubscribeView(View):
    def post(self, request):
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            from .models import NewsletterSubscription
            sub, created = NewsletterSubscription.objects.get_or_create(
                email=form.cleaned_data["email"]
            )
            if created:
                messages.success(request, f"Assinatura confirmada para {sub.email}.")
            else:
                messages.info(request, "Este e-mail já está inscrito.")
            return redirect("app1:home")
        messages.error(request, "Verifique o e-mail informado.")
        noticias = Noticia.objects.order_by('-data_publicacao')[:10]
        context = {"form": form, 'noticias': noticias}
        return render(request, "app1/home.html", context)

class SearchView(View):
    def get(self, request):
        q = request.GET.get("q", "").strip()
        resultados = []

        if q:
            resultados = Noticia.objects.filter(
                Q(titulo__icontains=q) | Q(conteudo__icontains=q)
            ).order_by('-data_publicacao')

        favoritos_ids = request.session.get('favoritos', [])

        contexto = {
            "form": SubscriptionForm(),
            "query": q,
            "results": resultados,   
            "favoritos_ids": favoritos_ids,
        }

        return render(request, "app1/resultado_pesquisa.html", contexto)

def detalhe_noticia(request, pk):
    noticia = get_object_or_404(Noticia, pk=pk)
    favoritos_ids = request.session.get('favoritos', [])
    is_favorita = pk in favoritos_ids
    contexto = {
        'noticia': noticia,
        'is_favorita': is_favorita
    }
    return render(request, 'app1/noticia_detalhe.html', contexto)

def visualizar_categorias(request):
    categorias = Categoria.objects.order_by('nome')
    context = {'categorias': categorias}
    return render(request, 'app1/categorias.html', context)

def categoria_filtro(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    noticias = Noticia.objects.filter(categoria=categoria).order_by('titulo')
    favoritos_ids = request.session.get('favoritos', [])
    contexto = {
        'noticias': noticias,
        'categoria': categoria,
        'favoritos_ids': favoritos_ids
    }
    return render(request, 'app1/home.html', contexto)

class FavoritosListView(ListView):
    model = Noticia
    template_name = 'app1/meus_favoritos.html'
    context_object_name = 'noticias'

    def get_queryset(self):
        favoritos_ids = self.request.session.get('favoritos', [])
        return Noticia.objects.filter(id__in=favoritos_ids).order_by('-data_publicacao')

@require_POST
def favoritar_noticia_view(request, pk):
    noticia = get_object_or_404(Noticia, pk=pk)
    favoritos = request.session.get('favoritos', [])
    if pk in favoritos:
        favoritos.remove(pk)
        messages.info(request, "Notícia removida dos favoritos.")
    else:
        favoritos.append(pk)
        messages.success(request, "Notícia adicionada aos favoritos.")
    request.session['favoritos'] = favoritos
    return redirect(request.META.get('HTTP_REFERER', 'app1:home'))

