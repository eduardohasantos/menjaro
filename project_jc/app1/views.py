from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Noticia, Categoria, Comentario
from .forms import SubscriptionForm, RegisterForm, ComentarioForm
from django.views.generic import ListView
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.http import FileResponse
from .utils.pdf_utils import gerar_pdf_noticia

class HomeView(View):
    def get(self, request):
        noticias = Noticia.objects.order_by('-data_publicacao')
        favoritos_ids = []

        if request.user.is_authenticated:
            favoritos_ids = request.user.noticias_favoritas.values_list('id', flat=True)

        context = {
            "form": SubscriptionForm(),
            "noticias": noticias,
            "favoritos_ids": favoritos_ids,
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

        messages.error(request, "Email já cadastrado")
        noticias = Noticia.objects.order_by('-data_publicacao')[:10]
        return render(request, "app1/home.html", {"form": form, 'noticias': noticias})


class SearchView(View):
    def get(self, request):
        q = request.GET.get("q", "").strip()
        resultados = []

        if q:
            resultados = Noticia.objects.filter(
                Q(titulo__icontains=q) | Q(conteudo__icontains=q)
            ).order_by('-data_publicacao')

        favoritos_ids = []
        if request.user.is_authenticated:
            favoritos_ids = request.user.noticias_favoritas.values_list('id', flat=True)

        contexto = {
            "form": SubscriptionForm(),
            "query": q,
            "results": resultados,
            "favoritos_ids": favoritos_ids,
        }
        return render(request, "app1/resultado_pesquisa.html", contexto)


def detalhe_noticia(request, pk):
    noticia = get_object_or_404(Noticia, pk=pk)

    if request.user.is_authenticated:
        if request.user not in noticia.usuarios_que_visitaram.all():
            noticia.visualizacoes += 1
            noticia.usuarios_que_visitaram.add(request.user)
            noticia.save()
        is_favorita = noticia.favoritos.filter(id=request.user.id).exists()
    else:
        noticia.visualizacoes += 1
        noticia.save()
        is_favorita = False

    filtro = request.GET.get("filtro", "")
    comentarios = noticia.comentarios.all()
    if filtro == "recentes":
        comentarios = comentarios.order_by("-data_comentario")
    elif filtro == "antigos":
        comentarios = comentarios.order_by("data_comentario")
    elif filtro == "meus" and request.user.is_authenticated:
        comentarios = comentarios.filter(usuario=request.user)

    form_comentario = ComentarioForm()

    return render(request, "app1/noticia_detalhe.html", {
        "noticia": noticia,
        "comentarios": comentarios,
        "form_comentario": form_comentario,
        "is_favorita": is_favorita,
    })



@require_POST
@login_required(login_url='/accounts/login/')
def adicionar_comentario(request, pk):
    noticia = get_object_or_404(Noticia, pk=pk)
    form = ComentarioForm(request.POST)

    if form.is_valid():
        comentario = form.save(commit=False)
        comentario.noticia = noticia
        comentario.usuario = request.user
        comentario.save()
        messages.success(request, "💬 Seu comentário foi publicado com sucesso!")
    else:
        messages.error(request, "⚠️ Ocorreu um erro ao enviar seu comentário.")

    return redirect('app1:detalhe_noticia', pk=pk)


def visualizar_categorias(request):
    categorias = Categoria.objects.order_by('nome')
    return render(request, 'app1/categorias.html', {'categorias': categorias})


def categoria_filtro(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    noticias = Noticia.objects.filter(categoria=categoria).order_by('-data_publicacao')
    favoritos_ids = []
    if request.user.is_authenticated:
        favoritos_ids = request.user.noticias_favoritas.values_list('id', flat=True)

    contexto = {'noticias': noticias, 'categoria': categoria, 'favoritos_ids': favoritos_ids}
    return render(request, 'app1/home.html', contexto)


class FavoritosListView(ListView):
    model = Noticia
    template_name = 'app1/meus_favoritos.html'
    context_object_name = 'noticias'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.request.user.noticias_favoritas.all().order_by('-data_publicacao')
        return Noticia.objects.none()


@login_required(login_url='/accounts/login/')
def favoritar_noticia_view(request, pk):
    noticia = get_object_or_404(Noticia, pk=pk)
    if noticia.favoritos.filter(id=request.user.id).exists():
        noticia.favoritos.remove(request.user)
        messages.info(request, "💔 Notícia removida dos favoritos.")
    else:
        noticia.favoritos.add(request.user)
        messages.success(request, "⭐ Notícia adicionada aos favoritos!")
    return redirect(request.META.get('HTTP_REFERER', 'app1:home'))


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "🎉 Registro concluído com sucesso! Bem-vindo(a).")
            return redirect('app1:home')
        else:
            messages.error(request, "Erro no registro. Verifique os campos.")
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def editar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)

    if request.method == 'POST':
        form = ComentarioForm(request.POST, instance=comentario)
        if form.is_valid():
            form.save()
        return redirect('app1:detalhe_noticia', pk=comentario.noticia.id) # redireciona sempre após POST
    else:
        form = ComentarioForm(instance=comentario)

    return render(request, 'app1/editar_comentario.html', {'form': form, 'comentario': comentario})

@login_required

def excluir_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)
    if request.user == comentario.usuario or request.user.is_staff:
        comentario.delete()
        messages.success(request, "Comentário excluído com sucesso!")
    else:
        messages.error(request, "Você não tem permissão para excluir este comentário.")
    return redirect('app1:detalhe_noticia', pk=comentario.noticia.pk)


def baixar_pdf_noticia(request, pk):
    noticia = get_object_or_404(Noticia, pk=pk)
    pdf_buffer = gerar_pdf_noticia(noticia)

    filename = f"noticia_{noticia.id}.pdf"
    return FileResponse(pdf_buffer, as_attachment=True, filename=filename)