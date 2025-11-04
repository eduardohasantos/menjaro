from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Noticia, Categoria
from .forms import SubscriptionForm
from django.views.generic import ListView
from django.views.decorators.http import require_POST

class HomeView(View):
    def get(self, request):
        noticias = Noticia.objects.order_by('-data_publicacao')
        favoritos_ids = []
        if hasattr(request.user, 'noticias_favoritas'):
            favoritos_ids = request.user.noticias_favoritas.values_list('id', flat=True)
        context = {
            "form": SubscriptionForm(),
            'noticias': noticias,
            'favoritos_ids': favoritos_ids
        }
        return render(request, "app1/home.html", context)

class SubscribeView(View):
    def post(self, request):
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            sub, created = form.save(commit=False), False
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
        noticias_encontradas = Noticia.objects.filter(titulo__icontains=q)
        favoritos_ids = []
        if hasattr(request.user, 'noticias_favoritas'):
            favoritos_ids = request.user.noticias_favoritas.values_list('id', flat=True)
        ctx = {
            "form": SubscriptionForm(),
            "query": q,
            "noticias": noticias_encontradas,
            'favoritos_ids': favoritos_ids
        }
        return render(request, "app1/home.html", ctx)

def detalhe_noticia(request, pk):
    noticia = get_object_or_404(Noticia, pk=pk)
    is_favorita = False
    if hasattr(request.user, 'id') and request.user.id:
        is_favorita = noticia.favoritos.filter(id=request.user.id).exists()
    contexto = {
        'noticia': noticia,
        'is_favorita': is_favorita
    }
    return render(request, 'app1/noticia_detalhe.html', contexto)

def visualizar_categorias(requests):
    categorias = Categoria.objects.order_by('nome')
    context = {'categorias': categorias}
    return render(requests, 'app1/categorias.html', context)

def categoria_filtro(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    noticias = Noticia.objects.filter(categoria=categoria).order_by('titulo')
    favoritos_ids = []
    if hasattr(request.user, 'noticias_favoritas'):
        favoritos_ids = request.user.noticias_favoritas.values_list('id', flat=True)
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
        if hasattr(self.request.user, 'noticias_favoritas'):
            return self.request.user.noticias_favoritas.all().order_by('-data_publicacao')
        return Noticia.objects.none()

@require_POST
def favoritar_noticia_view(request, pk):
    noticia = get_object_or_404(Noticia, pk=pk)
    if not request.user.is_authenticated:
        messages.error(request, "Você precisa estar logado para favoritar notícias.")
        return redirect(request.META.get('HTTP_REFERER', 'app1:home'))
    if request.user in noticia.favoritos.all():
        noticia.favoritos.remove(request.user)
        messages.info(request, "Notícia removida dos favoritos.")
    else:
        noticia.favoritos.add(request.user)
        messages.success(request, "Notícia adicionada aos favoritos.")
    return redirect(request.META.get('HTTP_REFERER', 'app1:home'))
