from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Noticia
from .forms import SubscriptionForm

class HomeView(View):
    def get(self, request):
        noticias = Noticia.objects.order_by('-data_publicacao')
        context = {"form": SubscriptionForm(), 'noticias': noticias}
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
        return render(request, "app1/home.html", {"form": form})

class SearchView(View):
    def get(self, request):
        q = request.GET.get("q", "").strip()
        # Integração com seus models de notícia quando existirem:
        results = []  # ex.: News.objects.filter(title__icontains=q)
        ctx = {"form": SubscriptionForm(), "query": q, "results": results}
        return render(request, "app1/home.html", ctx)
    

def detalhe_noticia(request, pk):
    """
    Exibe uma única notícia com base na sua chave primária (pk).
    """

    noticia = get_object_or_404(Noticia, pk=pk)
    
    contexto = {
        'noticia': noticia
    }
    return render(request, 'app1/noticia_detalhe.html', contexto)

    # from django.shortcuts import render
    # from django.http import HttpResponse

    # def home(request):
    #     return HttpResponse("Created first APP")
    # Create your views here.
