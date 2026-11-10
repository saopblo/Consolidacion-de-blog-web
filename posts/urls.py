from django.urls import path
from posts import views


urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('acerca/', views.acerca, name='acerca'),
    path('posts/', views.lista_posts, name='lista_posts'),
    path('posts/crear/', views.CrearPostView.as_view(), name='crear_post'),
    path('posts/<slug:slug>/', views.detalle_post, name='detalle_post'),
    path('posts/<slug:slug>/editar/', views.EditarPostView.as_view(), name='editar_post'),
    path('posts/<slug:slug>/eliminar/', views.EliminarPostView.as_view(), name='eliminar_post'),
    path('posts/<slug:slug>/comentar/', views.agregar_comentario, name='agregar_comentario'),
]
