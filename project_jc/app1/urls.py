from django.urls import path
from .views import HomeView, SubscribeView, SearchView, detalhe_noticia, visualizar_categorias,categoria_filtro
from . import views
app_name = "app1"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path('noticia/<int:pk>/', detalhe_noticia, name='detalhe_noticia'),
    path("subscribe/", SubscribeView.as_view(), name="subscribe"),
    path("search/", SearchView.as_view(), name="search"),
    path("categorias/",visualizar_categorias, name = 'categorias' ),
    path("categorias/<int:pk>",categoria_filtro, name = 'categoria_filtro' ),
    path('meus-favoritos/', views.FavoritosListView.as_view(), name='meus_favoritos'),
    path('noticia/<int:pk>/favoritar/', views.favoritar_noticia_view, name='favoritar_noticia_view'),
    path('noticia/<int:pk>/comentar/', views.adicionar_comentario, name='adicionar_comentario'),
]


