
from django import forms
from .models import Comment, Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['titulo', 'contenido', 'estado', 'imagen']
        labels = {
            'titulo': 'Título',
            'contenido': 'Contenido',
            'estado': 'Estado',
            'imagen': 'Imagen',
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['contenido']
        labels = {
            'contenido': 'Tu comentario',
        }
        widgets = {
            'contenido': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Escribe tu comentario...',
            }),
        }
