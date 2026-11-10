from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
AUTH_USER_MODEL = get_user_model()

class Post(models.Model):
    ESTADOS = [
        ("borrador", "Borrador"),
        ("publicado", "Publicado"),
        ("archivado", "Archivado"),
    ]
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    autor = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="borrador")
    imagen= models.ImageField(upload_to='posts/', null=True, blank=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-fecha_creacion"]

    def __str__(self):
        return self.titulo


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comentarios")
    autor = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comentarios")
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha_creacion"]

    def __str__(self):
        return self.contenido[:50]
