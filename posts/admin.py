from django.contrib import admin
from .models import Post


admin.site.site_header = "Administracion de mi blog"

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("titulo", "fecha_creacion", "estado","autor")
    search_fields = ("titulo", "contenido")
    list_filter = ("estado", "fecha_creacion")


