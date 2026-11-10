from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import CharField, Q
from django.db.models.functions import Cast
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.decorators.http import require_POST
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import Http404
from .models import Post
from .forms import PostForm, CommentForm


def inicio(request):
    criterio = request.GET.get('q')

    if request.user.is_authenticated:
        posts = Post.objects.filter(Q(estado='publicado') | Q(autor=request.user))
    else:
        posts = Post.objects.filter(estado='publicado')

    if criterio:
        posts = posts.annotate(
            fecha_creacion_texto=Cast("fecha_creacion", output_field=CharField())
        )
        posts = posts.filter(
            Q(titulo__icontains=criterio)
            | Q(contenido__icontains=criterio)
            | Q(autor__username__icontains=criterio)
            | Q(autor__first_name__icontains=criterio)
            | Q(autor__last_name__icontains=criterio)
            | Q(fecha_creacion_texto__icontains=criterio)
        )

    posts = posts.order_by('-fecha_creacion')

    contexto_inicio = {
        'titulo': 'Página de Inicio',
        'seccion': 'Principal',
        'criterio': criterio,
        'posts': posts,
    }

    return render(request, "posts/inicio.html", contexto_inicio)


def acerca(request):
    contexto_acerca = { 'titulo': 'Acerca de', 'seccion': 'Acerca' }
    return render(request, "posts/acerca.html", contexto_acerca)

def lista_posts(request):
    if request.user.is_authenticated:
        posts = Post.objects.filter(Q(estado='publicado') | Q(autor=request.user))
    else:
        posts = Post.objects.filter(estado='publicado')

    posts = posts.order_by("-fecha_creacion")

    contexto = {
        'posts':posts,
    }
    return render(request, "posts/lista_posts.html", contexto)


class CrearPostView(LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = "posts/post_form.html"
    success_url = reverse_lazy("inicio")
    extra_context = {
        "titulo_pagina": "Crear un post",
        "texto_boton": "Crear",
    }


    def form_valid(self, form):
        form.instance.autor = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, "El post fue creado correctamente")
        return response

def detalle_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if not puede_ver_post(request, post):
        raise Http404("No tienes permiso para ver este post.")

    return render(request, "posts/detalle_post.html", {
        "post": post,
        "form": CommentForm(),
    })


def puede_ver_post(request, post):
    return post.estado == "publicado" or (
        request.user.is_authenticated and request.user == post.autor
    )

class EditarPostView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "posts/post_form.html"
    context_object_name = "post"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    extra_context = {
        "titulo_pagina": "Editar un post",
        "texto_boton": "Editar",
    }
    raise_exception = True

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.autor

    def get_success_url(self):
        return reverse_lazy("detalle_post", kwargs={"slug": self.object.slug})

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "El post fue editado correctamente")
        return response


class EliminarPostView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "posts/post_confirm_delete.html"
    context_object_name = "post"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    success_url = reverse_lazy("inicio")
    raise_exception = True

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.autor

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.warning(self.request, "El post fue eliminado correctamente")
        return response

@login_required
@require_POST
def agregar_comentario(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if not puede_ver_post(request, post):
        raise Http404("No tienes permiso para comentar este post.")
    form = CommentForm(request.POST)
    if form.is_valid():
        comentario = form.save(commit=False)
        comentario.post = post
        comentario.autor = request.user
        comentario.save()
        messages.success(request, "El comentario fue agregado correctamente")
        return redirect("detalle_post", slug=post.slug)

    return render(request, "posts/detalle_post.html", {
        "post": post,
        "form": form,
    })
