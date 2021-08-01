from django.urls import path

from . import views
app_name = "enc"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.entries, name="entries"),
    path('search', views.search, name='search'),
    path('random', views.random_result, name='random'),
    path('create', views.create_page, name='create'),
    path('edit', views.edit_page, name='edit'),
    path("save",views.save_page, name="save")
]
