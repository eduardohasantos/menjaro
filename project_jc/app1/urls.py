from django.urls import path
from .views import HomeView, SubscribeView, SearchView

app_name = "app1"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("subscribe/", SubscribeView.as_view(), name="subscribe"),
    path("search/", SearchView.as_view(), name="search"),
]
