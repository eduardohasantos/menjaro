from django.urls import path
from .views import (
    HomeView, SubscribeView, SearchView, detalhe_noticia, visualizar_categorias,
    categoria_filtro, FavoritosListView, favoritar_noticia_view,
    adicionar_comentario, editar_comentario, excluir_comentario
)
from django.conf import settings
from django.conf.urls.static import static
from . import views
app_name = "app1"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("subscribe/", SubscribeView.as_view(), name="subscribe"),
    path("search/", SearchView.as_view(), name="search"),

    path('noticia/<int:pk>/', views.detalhe_noticia, name='detalhe_noticia'),
    path("noticia/<int:pk>/favoritar/", favoritar_noticia_view, name="favoritar_noticia_view"),
    path("noticia/<int:pk>/comentar/", adicionar_comentario, name="adicionar_comentario"),

    path("categorias/", visualizar_categorias, name="categorias"),
    path("categorias/<int:pk>/", categoria_filtro, name="categoria_filtro"),

    path("meus-favoritos/", FavoritosListView.as_view(), name="meus_favoritos"),

    path('comentario/<int:comentario_id>/editar/', views.editar_comentario, name='editar_comentario'),
    path('comentario/<int:comentario_id>/excluir/', views.excluir_comentario, name='excluir_comentario'),
    path('noticia/<int:pk>/pdf/', views.baixar_pdf_noticia, name="baixar_pdf_noticia"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
