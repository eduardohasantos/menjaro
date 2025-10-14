from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View

from .forms import SubscriptionForm


class HomeView(View):
    def get(self, request):
        return render(request, "app1/home.html", {"form": SubscriptionForm()})

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

# from django.shortcuts import render
# from django.http import HttpResponse

# def home(request):
#     return HttpResponse("Created first APP")
# Create your views here.
