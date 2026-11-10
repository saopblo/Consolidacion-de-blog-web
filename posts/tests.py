from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Comment, Post


class CrearPostViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="autora",
            password="test-password",
        )

    def test_crea_post_con_el_usuario_autenticado(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("crear_post"),
            {
                "titulo": "Post de prueba",
                "contenido": "Contenido de prueba",
                "estado": "borrador",
            },
        )

        self.assertRedirects(response, reverse("inicio"))
        post = Post.objects.get(titulo="Post de prueba")
        self.assertEqual(post.autor, self.user)
        self.assertEqual(
            [message.message for message in response.wsgi_request._messages],
            ["El post fue creado correctamente"],
        )

    def test_requiere_autenticacion(self):
        response = self.client.get(reverse("crear_post"))

        self.assertEqual(response.status_code, 302)


class EditarEliminarPostViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="autora",
            password="test-password",
        )
        self.post = Post.objects.create(
            titulo="Post original",
            contenido="Contenido original",
            estado="borrador",
            autor=self.user,
        )
        self.client.force_login(self.user)

    def test_edita_post_y_muestra_mensaje(self):
        response = self.client.post(
            reverse("editar_post", kwargs={"slug": self.post.slug}),
            {
                "titulo": "Post actualizado",
                "contenido": "Contenido actualizado",
                "estado": "publicado",
            },
        )

        self.post.refresh_from_db()
        self.assertRedirects(
            response,
            reverse("detalle_post", kwargs={"slug": self.post.slug}),
        )
        self.assertEqual(self.post.titulo, "Post actualizado")
        self.assertEqual(self.post.autor, self.user)
        self.assertEqual(
            [message.message for message in response.wsgi_request._messages],
            ["El post fue editado correctamente"],
        )

    def test_elimina_post_y_muestra_mensaje(self):
        response = self.client.post(
            reverse("eliminar_post", kwargs={"slug": self.post.slug}),
        )

        self.assertRedirects(response, reverse("inicio"))
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())
        self.assertEqual(
            [message.message for message in response.wsgi_request._messages],
            ["El post fue eliminado correctamente"],
        )

    def test_editar_y_eliminar_requieren_autenticacion(self):
        self.client.logout()

        edit_response = self.client.get(
            reverse("editar_post", kwargs={"slug": self.post.slug}),
        )
        delete_response = self.client.get(
            reverse("eliminar_post", kwargs={"slug": self.post.slug}),
        )

        self.assertEqual(edit_response.status_code, 403)
        self.assertEqual(delete_response.status_code, 403)

    def test_otro_usuario_no_puede_editar_ni_eliminar_el_post(self):
        otro_usuario = get_user_model().objects.create_user(username="otro")
        self.client.force_login(otro_usuario)

        edit_response = self.client.get(
            reverse("editar_post", kwargs={"slug": self.post.slug}),
        )
        delete_response = self.client.get(
            reverse("eliminar_post", kwargs={"slug": self.post.slug}),
        )

        self.assertEqual(edit_response.status_code, 403)
        self.assertEqual(delete_response.status_code, 403)


class ComentariosViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="comentarista")
        self.post = Post.objects.create(
            titulo="Post publicado",
            contenido="Contenido",
            estado="publicado",
            autor=self.user,
        )
        self.url = reverse("agregar_comentario", kwargs={"slug": self.post.slug})
        self.client.force_login(self.user)

    def test_detalle_muestra_seccion_y_formulario_de_comentarios(self):
        response = self.client.get(
            reverse("detalle_post", kwargs={"slug": self.post.slug}),
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Comentarios")
        self.assertContains(response, "Comentar")

    def test_agrega_comentario_y_redirige_al_post(self):
        response = self.client.post(self.url, {"contenido": "Buen artículo"})

        self.assertRedirects(
            response,
            reverse("detalle_post", kwargs={"slug": self.post.slug}),
        )
        comentario = Comment.objects.get()
        self.assertEqual(comentario.contenido, "Buen artículo")
        self.assertEqual(comentario.autor, self.user)
        self.assertEqual(comentario.post, self.post)

    def test_muestra_error_si_el_comentario_esta_vacio(self):
        response = self.client.post(self.url, {"contenido": ""})

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context["form"], "contenido", "Este campo es obligatorio.")
        self.assertFalse(Comment.objects.exists())
