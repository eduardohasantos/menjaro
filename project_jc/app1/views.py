from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Noticia, Categoria
from .forms import SubscriptionForm
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST

class HomeView(View):
    def get(self, request):
        noticias = Noticia.objects.order_by('-data_publicacao')
        favoritos_ids = []
        if request.user.is_authenticated:
            # Pega a lista de IDs das notícias favoritas do usuário
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
            # get_or_create para evitar erro de unique:
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

        noticias = Noticia.objects.order_by('-data_publicacao')[:10] # Limita em caso de erro
        context = {"form": form, 'noticias': noticias}
        return render(request, "app1/home.html", context)

class SearchView(View):
    def get(self, request):
        q = request.GET.get("q", "").strip()
        # Integração com seus models de notícia quando existirem:
        noticias_encontradas = Noticia.objects.filter(titulo__icontains=q)
        favoritos_ids = []
        if request.user.is_authenticated:
            favoritos_ids = request.user.noticias_favoritas.values_list('id', flat=True)

        ctx = {
            "form": SubscriptionForm(), 
            "query": q, 
            "noticias": noticias_encontradas, # Passa as notícias encontradas
            'favoritos_ids': favoritos_ids # Passa os IDs dos favoritos
        }
        return render(request, "app1/home.html", ctx)
    

def detalhe_noticia(request, pk):
    """
    Exibe uma única notícia com base na sua chave primária (pk).
    """

    noticia = get_object_or_404(Noticia, pk=pk)
    is_favorita = False
    if request.user.is_authenticated:
        is_favorita = noticia.favoritos.filter(id=request.user.id).exists()
    
    contexto = {
        'noticia': noticia,
        'is_favorita': is_favorita # Passa para o template de detalhe
    }
    return render(request, 'app1/noticia_detalhe.html', contexto)


def visualizar_categorias(requests):
    categorias = Categoria.objects.order_by('nome')
    context = {'categorias': categorias}

    return render(requests, 'app1/categorias.html', context)



def categoria_filtro(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)

    # Filtra as notícias da categoria e ordena por título
    noticias = Noticia.objects.filter(
        categoria=categoria
    ).order_by('titulo')

    favoritos_ids = []
    if request.user.is_authenticated:
        favoritos_ids = request.user.noticias_favoritas.values_list('id', flat=True)

    contexto = {
        'noticias': noticias,
        'categoria': categoria,
        'favoritos_ids': favoritos_ids # Passa os IDs dos favoritos
    }
    return render(request, 'app1/home.html', contexto)



class FavoritosListView(ListView):
    model = Noticia
    template_name = 'app1/meus_favoritos.html' 
    context_object_name = 'noticias'

    def get_queryset(self):
        # Filtra o queryset para pegar apenas as 'noticias_favoritas'
        # do usuário que está fazendo a requisição (request.user)
        return self.request.user.noticias_favoritas.all().order_by('-data_publicacao')


@require_POST   # Garante que esta view só aceite requisições POST
def favoritar_noticia_view(request, pk):
    
    #View que processa a ação de favoritar ou desfavoritar.
    noticia = get_object_or_404(Noticia, pk=pk)

    # Verifica se o usuário (request.user) JÁ favoritou esta notícia
    if request.user in noticia.favoritos.all():
        # Se sim, remove o favorito
        noticia.favoritos.remove(request.user)
    else:
        # Se não, adiciona o favorito
        noticia.favoritos.add(request.user)

    # Redireciona o usuário de volta para a página de onde ele veio.
    return redirect(request.META.get('HTTP_REFERER', 'app1:home'))
