from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    
    #Código autoral abaixo:
    path("wiki/<str:title>", views.entry, name="entry"),
    path("create", views.create, name="create"),
    path("search", views.search, name="search"),
    path("wiki/edit/<str:title>", views.edit, name="edit"),
    path("randomize", views.randomize, name="randomize")
]
